import os
import re
import sys
import json
import socket
import time
import subprocess
from pathlib import Path

# Setup base paths
EXECUTION_DIR = Path(__file__).parent
BASE_DIR = EXECUTION_DIR.parent
BUILDS_DIR = BASE_DIR / ".tmp" / "builds"

def parse_hex_color(color_str: str) -> tuple:
    """Parses a hex color string or returns None if invalid."""
    color_str = color_str.strip()
    if color_str.startswith("#"):
        hex_val = color_str[1:]
        if len(hex_val) == 3:
            hex_val = "".join([c * 2 for c in hex_val])
        if len(hex_val) == 6:
            return (int(hex_val[0:2], 16), int(hex_val[2:4], 16), int(hex_val[4:6], 16))
    elif color_str.startswith("rgba"):
        # Match digits inside rgba
        match = re.match(r"rgba?\s*\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)", color_str)
        if match:
            return (int(match.group(1)), int(match.group(2)), int(match.group(3)))
    elif color_str.startswith("rgb"):
        match = re.match(r"rgb?\s*\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)", color_str)
        if match:
            return (int(match.group(1)), int(match.group(2)), int(match.group(3)))
    return None

def calculate_relative_luminance(rgb: tuple) -> float:
    """Calculates the relative luminance of an RGB color per WCAG 2.1."""
    channels = []
    for c in rgb:
        srgb = c / 255.0
        if srgb <= 0.03928:
            channels.append(srgb / 12.92)
        else:
            channels.append(((srgb + 0.055) / 1.055) ** 2.4)
    return 0.2126 * channels[0] + 0.7152 * channels[1] + 0.0722 * channels[2]

def calculate_contrast_ratio(color1: str, color2: str) -> float:
    """Calculates the WCAG contrast ratio between two color strings."""
    rgb1 = parse_hex_color(color1)
    rgb2 = parse_hex_color(color2)
    
    if not rgb1 or not rgb2:
        return 1.0  # Fallback for parsing errors
        
    l1 = calculate_relative_luminance(rgb1)
    l2 = calculate_relative_luminance(rgb2)
    
    lighter = max(l1, l2)
    darker = min(l1, l2)
    
    return (lighter + 0.05) / (darker + 0.05)

def check_port_open(host="127.0.0.1", port=3000) -> bool:
    """Checks if a port is open locally."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(1.0)
        try:
            s.connect((host, port))
            return True
        except Exception:
            return False

def run_performance_checker(session_id: str) -> dict:
    """
    Runs dynamic and static performance + accessibility checks on the built Next.js application.
    """
    print(f"\n==================================================")
    print(f"[AUDIT] RUNNING PERFORMANCE & WCAG CHECKER")
    print(f"Session ID: {session_id}")
    
    build_dir = BUILDS_DIR / session_id
    if not build_dir.exists():
        raise FileNotFoundError(f"Build directory not found at {build_dir}")
        
    report = {
        "lighthouse_score_estimation": 90,
        "wcag_compliance": {
            "contrast_ratios": {},
            "semantic_html": {"passed": True, "details": []},
            "a11y_accessibility": {"passed": True, "details": []}
        },
        "browser_audit": {
            "loaded_successfully": False,
            "console_errors": [],
            "screenshot_path": None
        },
        "warnings": []
    }
    
    # 1. Color Contrast Validation (static globals.css parsing)
    globals_css = build_dir / "app" / "globals.css"
    if globals_css.exists():
        print(f"[AUDIT] Checking theme color contrast ratios...")
        content = globals_css.read_text(encoding="utf-8")
        
        # Regex to parse variables
        color_vars = {}
        matches = re.findall(r"--color-(\w+):\s*([^;]+);", content)
        for name, value in matches:
            color_vars[name] = value.strip()
            
        bg = color_vars.get("bg")
        fg = color_vars.get("fg")
        accent = color_vars.get("accent")
        muted = color_vars.get("muted")
        
        if bg and fg:
            contrast_fg = calculate_contrast_ratio(bg, fg)
            report["wcag_compliance"]["contrast_ratios"]["bg_vs_fg"] = {
                "ratio": round(contrast_fg, 2),
                "passed": contrast_fg >= 4.5
            }
            if contrast_fg < 4.5:
                report["warnings"].append(f"Contrast ratio between background ({bg}) and foreground ({fg}) is {round(contrast_fg, 2)}:1 (Failed WCAG AA 4.5:1 limit)")
                
        if bg and accent:
            contrast_acc = calculate_contrast_ratio(bg, accent)
            report["wcag_compliance"]["contrast_ratios"]["bg_vs_accent"] = {
                "ratio": round(contrast_acc, 2),
                "passed": contrast_acc >= 3.0
            }
            if contrast_acc < 3.0:
                report["warnings"].append(f"Contrast ratio between background ({bg}) and accent ({accent}) is {round(contrast_acc, 2)}:1 (Failed WCAG AA 3:1 graphical element limit)")
                
        if bg and muted:
            contrast_mut = calculate_contrast_ratio(bg, muted)
            report["wcag_compliance"]["contrast_ratios"]["bg_vs_muted"] = {
                "ratio": round(contrast_mut, 2),
                "passed": contrast_mut >= 3.0
            }
    
    # 2. Semantic HTML & Alt Text static scanner
    print(f"[AUDIT] Scanning React codebase for semantic structure & a11y details...")
    
    semantic_elements = ["<main", "<header", "<footer", "<section"]
    found_semantics = []
    
    jsx_files = list(build_dir.glob("components/*.jsx")) + [build_dir / "app" / "page.js"]
    
    has_img = False
    img_has_alt = True
    missing_alt_files = []
    
    has_interactive = False
    interactive_has_focus = True
    missing_focus_files = []
    
    for jsx_file in jsx_files:
        if not jsx_file.exists():
            continue
        code = jsx_file.read_text(encoding="utf-8")
        
        # Check semantics
        for elem in semantic_elements:
            if elem in code and elem not in found_semantics:
                found_semantics.append(elem)
                
        # Check standard <img> tag alt
        if "<img" in code:
            has_img = True
            # Check for lack of alt attribute
            img_tags = re.findall(r"<img[^>]*>", code)
            for tag in img_tags:
                if "alt=" not in tag:
                    img_has_alt = False
                    missing_alt_files.append(jsx_file.name)
                    
        # Check interactive buttons/links outline focus
        if "<button" in code or "<a " in code:
            has_interactive = True
            interactive_tags = re.findall(r"<(button|a)[^>]*>", code)
            for tag in interactive_tags:
                if "focus" not in tag and "outline" not in tag:
                    interactive_has_focus = False
                    missing_focus_files.append(jsx_file.name)
                    
    # Document semantic HTML findings
    report["wcag_compliance"]["semantic_html"]["details"] = found_semantics
    if "<main" not in found_semantics:
        report["wcag_compliance"]["semantic_html"]["passed"] = False
        report["warnings"].append("Missing semantic <main> tag in experience page tree.")
        
    # Document accessibility findings
    if has_img:
        report["wcag_compliance"]["a11y_accessibility"]["details"].append({
            "audit": "image_alt_tags",
            "passed": img_has_alt,
            "files": list(set(missing_alt_files))
        })
        if not img_has_alt:
            report["warnings"].append(f"Image elements missing 'alt' attributes in: {list(set(missing_alt_files))}")
            report["wcag_compliance"]["a11y_accessibility"]["passed"] = False
            
    if has_interactive:
        report["wcag_compliance"]["a11y_accessibility"]["details"].append({
            "audit": "interactive_focus_states",
            "passed": interactive_has_focus,
            "files": list(set(missing_focus_files))
        })
        if not interactive_has_focus:
            report["wcag_compliance"]["a11y_accessibility"]["passed"] = False
            
    # 3. agent-browser Dynamic Auditing
    print(f"[AUDIT] Setting up dynamic browser testing...")
    
    server_process = None
    port = 3000
    
    # Check if port 3000 is open. If not, start local dev server in background
    if not check_port_open("127.0.0.1", port):
        print(f"[AUDIT] Port {port} is closed. Booting dev server in the background...")
        try:
            # Install package dependencies if needed (first-time build run)
            node_modules = build_dir / "node_modules"
            if not node_modules.exists():
                print(f"[AUDIT] node_modules not found. Executing npm install...")
                subprocess.run("npm install", shell=True, cwd=build_dir, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                
            server_process = subprocess.Popen(
                "npm run dev",
                shell=True,
                cwd=build_dir,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            # Wait up to 8 seconds for Next.js dev server to bind to port
            for _ in range(16):
                time.sleep(0.5)
                if check_port_open("127.0.0.1", port):
                    break
        except Exception as e:
            report["warnings"].append(f"Failed to auto-start dev server: {e}")
            
    if check_port_open("127.0.0.1", port):
        print(f"[AUDIT] Next.js dev server detected on http://localhost:{port}/. Running agent-browser...")
        try:
            # Open local sunucu and save screenshot via agent-browser CLI
            screenshot_out_dir = build_dir
            screenshot_out_dir.mkdir(parents=True, exist_ok=True)
            log_file = build_dir / "agent_browser_out.txt"
            
            # Step 1: Open the URL (non-blocking daemon check, with 15s timeout)
            print("[AUDIT] Signalling agent-browser to open page...")
            subprocess.run(f'agent-browser open http://localhost:{port}', shell=True, timeout=15, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            # Wait for Next.js hydration and Framer Motion entrance animations to settle
            print("[AUDIT] Waiting 3.5 seconds for animations and rendering to settle...")
            time.sleep(3.5)
            
            # Step 2: Take screenshot and redirect stdout to file (with 15s timeout)
            print("[AUDIT] Taking screenshot...")
            subprocess.run(f'agent-browser screenshot > "{log_file}" 2>&1', shell=True, timeout=15)
            
            # Read stdout from the redirect file
            res_stdout = ""
            if log_file.exists():
                res_stdout = log_file.read_text(encoding="utf-8")
                try:
                    log_file.unlink()
                except Exception:
                    pass
            
            # Check output for screenshot path
            screenshot_match = re.search(r"Screenshot saved to ([^\s\r\n]+)", res_stdout)
            if screenshot_match:
                src_screenshot = Path(screenshot_match.group(1))
                dest_screenshot = build_dir / "screenshot.png"
                if src_screenshot.exists():
                    if dest_screenshot.exists():
                        dest_screenshot.unlink()
                    src_screenshot.rename(dest_screenshot)
                    report["browser_audit"]["loaded_successfully"] = True
                    report["browser_audit"]["screenshot_path"] = str(dest_screenshot)
                    print(f"[AUDIT] Browser verification success! Visual output saved: {dest_screenshot}")
                else:
                    report["warnings"].append(f"Screenshot path parsed but file not found on disk: {src_screenshot}")
            else:
                report["warnings"].append(f"Could not find screenshot path in agent-browser output. Output: {res_stdout[:300]}")
        except subprocess.TimeoutExpired as te:
            report["warnings"].append(f"agent-browser execution timed out: {te}")
            print(f"[WARNING] agent-browser timed out.")
        except Exception as e:
            report["warnings"].append(f"Error during agent-browser execution: {e}")

    else:
        report["warnings"].append("Could not connect to Next.js dev server. Dynamic visual verification was bypassed.")
        
    # Clean up dev server process if we launched it
    if server_process:
        print("[AUDIT] Shutting down background dev server process...")
        if sys.platform == "win32":
            subprocess.run(f"taskkill /F /T /PID {server_process.pid}", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        else:
            server_process.terminate()
            
    # Compile final lighthouse estimation score based on warnings
    deductions = len(report["warnings"]) * 4
    report["lighthouse_score_estimation"] = max(60, 100 - deductions)
    
    print(f"[AUDIT COMPLETE] Est. Lighthouse Score: {report['lighthouse_score_estimation']}/100")
    print(f"Warnings flagged: {len(report['warnings'])}")
    print(f"==================================================\n")
    
    return report

if __name__ == "__main__":
    # Test checking build
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--session", type=str, default="test_run_next_app")
    args = parser.parse_args()
    
    try:
        rep = run_performance_checker(args.session)
        print(json.dumps(rep, indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"Error: {e}")
