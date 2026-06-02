import os
import json
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

def get_directive() -> str:
    """Reads the art-direction directive."""
    directive_path = Path(__file__).parent.parent / "directives" / "art-direction.md"
    if not directive_path.exists():
        directive_path = Path(__file__).parent.parent / "skills" / "art-director" / "SKILL.md"
    if not directive_path.exists():
        raise FileNotFoundError("Directive art-direction not found.")
    return directive_path.read_text(encoding="utf-8")

def execute_art_director(enriched_tokens: dict, brand_identity: dict, critic_feedback: str = "", model: str = "anthoring/claude-3-haiku") -> dict:
    """
    Executes the Art Director agent, taking design tokens and brand strategy, and returning a Visual Language style JSON.
    """
    # OpenRouter handles model names. Let's make sure model is a valid OpenRouter model, like anthropic/claude-3-haiku
    if "anthoring" in model: # safety fix for typo
        model = "anthropic/claude-3-haiku"
    print(f"[API CALL] Art Director generating visual tokens using {model}...")
    
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=OPENROUTER_API_KEY,
    )
    
    system_prompt = get_directive()
    
    user_content = f"Resolved Design Tokens:\n{json.dumps(enriched_tokens, indent=2)}\n\n"
    user_content += f"Brand Strategy:\n{json.dumps(brand_identity, indent=2)}\n\n"
    if critic_feedback:
        user_content += f"CRITIC FEEDBACK FOR REVISION:\n{critic_feedback}\n\nPlease adjust the visual tokens to address this critique.\n\n"
    user_content += "Generate the Visual Language JSON. Remember to output ONLY valid JSON, with NO other text or explanation."
    
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content}
        ]
    )
    
    raw_output = response.choices[0].message.content.strip()
    
    if raw_output.startswith("```json"):
        raw_output = raw_output[7:]
    if raw_output.startswith("```"):
        raw_output = raw_output[3:]
    if raw_output.endswith("```"):
        raw_output = raw_output[:-3]
        
    try:
        visual_language = json.loads(raw_output.strip())
        return visual_language
    except json.JSONDecodeError as e:
        print(f"[ERROR] Art Director outputted invalid JSON: {e}")
        print(f"Raw Output:\n{raw_output}")
        # Fallback based on colors solved in tokens
        colors = enriched_tokens.get("colors", {})
        typo = enriched_tokens.get("typography", {})
        return {
            "visual_mood": "Refined minimalist design with sleek accent hues.",
            "color_tokens": {
                "background": colors.get("background", "#0F0F0F"),
                "foreground": colors.get("foreground", "#FFFFFF"),
                "primary_accent": colors.get("accent", "#D4AF37"),
                "secondary_accent": colors.get("muted", "#A8A8A8"),
                "muted": "#1F1F1F",
                "border": "rgba(255,255,255,0.08)",
                "card_background": "rgba(255,255,255,0.03)"
            },
            "typography_tokens": {
                "header_font": typo.get("header_font", "Playfair Display"),
                "body_font": typo.get("body_font", "Inter"),
                "header_weight": typo.get("header_weight", "700"),
                "body_weight": typo.get("body_weight", "400"),
                "letter_spacing": typo.get("letter_spacing", "-0.01em"),
                "base_font_size": "16px"
            },
            "ui_tokens": {
                "border_radius": "12px",
                "border_width": "1px",
                "box_shadow": "0 10px 30px -10px rgba(0,0,0,0.5)",
                "backdrop_blur": "8px"
            },
            "hero_visual_style": "minimalist-split"
        }

if __name__ == "__main__":
    sample_tokens = {
        "brand": {"archetype": "rebel"},
        "colors": {"background": "#0F0F0F", "foreground": "#FFFFFF", "accent": "#CCFF00", "muted": "#888"},
        "typography": {"header_font": "Space Grotesk", "body_font": "Inter", "header_weight": "700", "body_weight": "400", "letter_spacing": "-0.02em"}
    }
    sample_brand = {"brand_name": "VANDAL"}
    print(json.dumps(execute_art_director(sample_tokens, sample_brand), indent=2, ensure_ascii=False))
