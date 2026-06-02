import os
import json
from pathlib import Path

def generate_theme(visual_language: dict, target_file: Path):
    """
    Reads visual language tokens and generates a tailored globals.css
    with dynamic CSS custom properties and dynamic Google Fonts imports.
    """
    print(f"[THEME ENGINE] Compiling visual language tokens into dynamic CSS variables...")
    
    # 1. Extract tokens
    color_tokens = visual_language.get("color_tokens", {})
    typography_tokens = visual_language.get("typography_tokens", {})
    ui_tokens = visual_language.get("ui_tokens", {})
    
    # Extract Google Fonts import url
    fonts_import = visual_language.get("fonts_import", "https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600&family=Inter:wght@400;500;700&display=swap")
    # If font import doesn't start with @import, wrap it
    if fonts_import and not fonts_import.startswith("@import"):
        fonts_import = f"@import url('{fonts_import}');"
        
    # 2. Map color configurations with fallback values
    bg = color_tokens.get("background", "#0D0D0D")
    fg = color_tokens.get("foreground", "#F5F5F0")
    accent = color_tokens.get("primary_accent", "#C5A880")
    muted = color_tokens.get("muted", "#404040")
    border = color_tokens.get("border", "rgba(255,255,255,0.08)")
    card_bg = color_tokens.get("card_background", "rgba(255,255,255,0.05)")
    
    # 3. Map typographic family names
    header_font = typography_tokens.get("header_font", "Playfair Display")
    body_font = typography_tokens.get("body_font", "Inter")
    
    # 4. Map spatial/UI tokens
    border_radius = ui_tokens.get("border_radius", "clamp(0.5rem, 1vw, 1rem)")
    border_width = ui_tokens.get("border_width", "0.5px")
    box_shadow = ui_tokens.get("box_shadow", "0px 20px 50px rgba(0,0,0,0.25)")
    backdrop_blur = ui_tokens.get("backdrop_blur", "12px")
    # Clean blur string if raw number
    if isinstance(backdrop_blur, (int, float)):
        backdrop_blur = f"{backdrop_blur}px"
    elif backdrop_blur and backdrop_blur.isdigit():
        backdrop_blur = f"{backdrop_blur}px"
    
    # 5. Build dynamic stylesheet content
    globals_css_content = f"""{fonts_import}

@tailwind base;
@tailwind components;
@tailwind utilities;

:root {{
  --color-bg: {bg};
  --color-fg: {fg};
  --color-accent: {accent};
  --color-muted: {muted};
  --color-border: {border};
  --color-card-bg: {card_bg};
  --border-radius: {border_radius};
  --border-width: {border_width};
  --box-shadow: {box_shadow};
  --backdrop-blur: {backdrop_blur};
  --font-header: '{header_font}', serif;
  --font-body: '{body_font}', sans-serif;
}}

/* Premium Reset & Global Styles */
body {{
  background-color: var(--color-bg);
  color: var(--color-fg);
  font-family: var(--font-body), sans-serif;
  overflow-x: hidden;
}}

/* Premium Scrollbars */
::-webkit-scrollbar {{
  width: 8px;
  height: 8px;
}}

::-webkit-scrollbar-track {{
  background: var(--color-bg);
}}

::-webkit-scrollbar-thumb {{
  background: var(--color-muted);
  border-radius: 4px;
}}

::-webkit-scrollbar-thumb:hover {{
  background: var(--color-accent);
}}

/* Selection Color */
::selection {{
  background-color: var(--color-accent);
  color: var(--color-bg);
}}
"""
    # Write to target
    target_file.parent.mkdir(parents=True, exist_ok=True)
    target_file.write_text(globals_css_content, encoding="utf-8")
    print(f"[THEME ENGINE] Successfully wrote dynamic globals.css to: {target_file}")

if __name__ == "__main__":
    # Test script dry run
    visual_sample = {
        "fonts_import": "https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600&family=Inter:wght@400;500;700&display=swap",
        "color_tokens": {
            "background": "#0D0D0D",
            "foreground": "#F5F5F0",
            "primary_accent": "#CCFF00",
            "border": "rgba(255,255,255,0.08)",
            "card_background": "rgba(255,255,255,0.05)"
        },
        "typography_tokens": {
            "header_font": "Space Grotesk",
            "body_font": "Inter"
        },
        "ui_tokens": {
            "border_radius": "8px",
            "border_width": "1px",
            "box_shadow": "0px 10px 30px rgba(0,0,0,0.5)",
            "backdrop_blur": "8px"
        }
    }
    
    test_path = Path(__file__).parent.parent / ".tmp" / "test_theme" / "globals.css"
    generate_theme(visual_sample, test_path)
