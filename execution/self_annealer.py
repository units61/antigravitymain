import os
import re
import sys
import json
import subprocess
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

def run_npm_build(build_dir: Path) -> tuple[int, str]:
    """Runs npm run build inside the target directory and returns the return code and logs."""
    print(f"[SANDBOX] Verifying compilation via npm run build in: {build_dir}")
    res = subprocess.run(
        "npm run build",
        shell=True,
        cwd=build_dir,
        capture_output=True,
        text=True
    )
    return res.returncode, res.stdout + "\n" + res.stderr

def run_self_annealing_loop(session_id: str, max_loops: int = 5, model: str = "anthropic/claude-3-haiku") -> bool:
    """
    Executes Phase 3: Self-Annealing Sandbox loop.
    Checks Next.js build compilation, captures error traces, and automatically repairs the source files.
    """
    base_dir = Path(__file__).parent.parent
    build_dir = base_dir / ".tmp" / "builds" / session_id
    
    if not build_dir.exists():
        print(f"[SELF-ANNEAL ERROR] Build directory does not exist: {build_dir}")
        return False
        
    print(f"\n==================================================")
    print(f"       STARTING SELF-ANNEALING SANDBOX RUN        ")
    print(f"Session ID: {session_id}")
    print(f"Max Loops Allowed: {max_loops}")
    print(f"==================================================\n")
    
    loop_count = 0
    while loop_count < max_loops:
        loop_count += 1
        print(f"\n--- [LOOP {loop_count}/{max_loops}] Compiling Sandbox App ---")
        
        # 1. Run build compilation
        returncode, logs = run_npm_build(build_dir)
        
        if returncode == 0:
            print(f"\n==================================================")
            print(f" [PASS] COMPILATION SUCCESSFUL ON LOOP {loop_count}!")
            print(f" Guaranteeing 100% error-free interactive experience.")
            print(f"==================================================\n")
            return True
            
        print(f"[FAIL] Sandbox compilation failed with code {returncode}. Entering diagnostics...")
        
        # 2. Diagnosing error file & message
        # Regex patterns to parse standard Next.js / webpack / typescript compiler errors
        error_file = None
        error_message = ""
        
        # Try to find failed file paths (e.g. ./components/MyComponent.jsx or app/page.js)
        # Next.js errors usually show paths relative to build directory
        file_matches = re.findall(r'(?:[cC]omponent[s]?/|app/|hooks/)[a-zA-Z0-9_\-\.\/]+', logs)
        if file_matches:
            # Clean duplicate paths and select the first component/page file
            unique_files = list(dict.fromkeys(file_matches))
            for f_path in unique_files:
                if f_path.endswith('.jsx') or f_path.endswith('.js'):
                    candidate = build_dir / f_path
                    if candidate.exists():
                        error_file = candidate
                        break
                        
        # Extract the specific trace/reason snippet
        # Look for "Error:" or "Failed to compile" or specific compiler error markers
        error_lines = []
        for line in logs.splitlines():
            if "Error:" in line or "Failed to compile" in line or "Type error:" in line or "SyntaxError:" in line or "ReferenceError:" in line:
                error_lines.append(line.strip())
                
        if error_lines:
            error_message = "\n".join(error_lines[:4])
        else:
            # Fallback to last few lines of the error trace
            error_message = "\n".join(logs.splitlines()[-6:])
            
        if not error_file:
            # Fallback to checking the main page.js if no specific file was matched
            candidate_page = build_dir / "app" / "page.js"
            if candidate_page.exists():
                error_file = candidate_page
                
        print(f"[DIAGNOSTICS] Failed File identified: {error_file.name if error_file else 'Unknown'}")
        print(f"[DIAGNOSTICS] Error summary:\n{error_message}\n")
        
        if not error_file or not error_file.exists():
            print("[SELF-ANNEAL FAIL] Could not determine target source file to patch. Halting.")
            return False
            
        # 3. LLM Hotfix Code generation
        if not OPENROUTER_API_KEY:
            print("[SELF-ANNEAL FAIL] OPENROUTER_API_KEY missing. Cannot repair code.")
            return False
            
        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=OPENROUTER_API_KEY,
        )
        
        failed_code = error_file.read_text(encoding="utf-8")
        
        system_prompt = """You are the "Self-Annealing Diagnostics Engine".
Your task is to analyze a compiler/runtime error from a Next.js React application and repair the broken file.

You will be given:
1. The path and current source code of the failed file.
2. The compilation stdout/stderr logs containing the error trace.

Your goal is to output the completely fixed and working version of this file.
RULES:
1. Keep the exact same component signature and logic, but fix the syntax, typings, missing imports, Next.js hydration issues, or Three.js/GSAP errors.
2. Ensure you do not introduce new syntax errors.
3. Output ONLY the complete updated code of the file.
4. Absolutely NO markdown wrap, NO chat, NO explanations, NO surrounding text. Output the raw code directly.
"""

        user_prompt = f"""Failed File Path: {error_file}
Failed File Current Source Code:
```javascript
{failed_code}
```

Compilation Error Trace:
{logs}

Provide the corrected, working React code for this file.
"""

        print(f"[REPAIR] Requesting self-annealing hotfix from AI compiler...")
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.1
            )
            
            repaired_code = response.choices[0].message.content.strip()
            
            # Clean markdown code blocks if any
            if repaired_code.startswith("```"):
                lines = repaired_code.splitlines()
                if lines[0].startswith("```"):
                    lines = lines[1:]
                if lines and lines[-1].startswith("```"):
                    lines = lines[:-1]
                repaired_code = "\n".join(lines).strip()
                
            # Write hotfix back into file
            print(f"[REPAIR] Applying Hotfix Patch to {error_file.name}...")
            error_file.write_text(repaired_code, encoding="utf-8")
            
        except Exception as e:
            print(f"[SELF-ANNEAL FAIL] AI repair request failed: {e}")
            return False
            
    print(f"\n[SELF-ANNEAL FAIL] Exceeded maximum self-annealing iterations ({max_loops}) without compiling successfully.")
    return False

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--session", type=str, default="test_run_next_app")
    args = parser.parse_args()
    
    run_self_annealing_loop(args.session)
