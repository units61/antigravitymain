import os
import json
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

def get_directive() -> str:
    """Reads the ux-architecture directive."""
    directive_path = Path(__file__).parent.parent / "directives" / "ux-architecture.md"
    if not directive_path.exists():
        raise FileNotFoundError("Directive ux-architecture not found.")
    return directive_path.read_text(encoding="utf-8")

def execute_ux_architect(enriched_tokens: dict, brand_identity: dict, visual_language: dict, critic_feedback: str = "", model: str = "anthropic/claude-3-haiku") -> dict:
    """
    Executes the UX Architect agent, building the page structure, layouts, and rich copywriting copy.
    """
    print(f"[API CALL] UX Architect constructing layout structure using {model}...")
    
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=OPENROUTER_API_KEY,
    )
    
    system_prompt = get_directive()
    
    user_content = f"Resolved Design Tokens:\n{json.dumps(enriched_tokens, indent=2)}\n\n"
    user_content += f"Brand Strategy:\n{json.dumps(brand_identity, indent=2)}\n\n"
    user_content += f"Visual Language Style:\n{json.dumps(visual_language, indent=2)}\n\n"
    if critic_feedback:
        user_content += f"CRITIC FEEDBACK FOR REVISION:\n{critic_feedback}\n\nPlease revise layout structure and copy to resolve this feedback.\n\n"
    user_content += "Generate the Experience Flow JSON. Remember to output ONLY valid JSON, with NO other text or explanation."
    
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
        ux_flow = json.loads(raw_output.strip())
        return ux_flow
    except json.JSONDecodeError as e:
        print(f"[ERROR] UX Architect outputted invalid JSON: {e}")
        print(f"Raw Output:\n{raw_output}")
        # Fallback template
        is_turkish = "turkish" in str(enriched_tokens).lower() or "sitem" in str(enriched_tokens).lower()
        name = brand_identity.get("brand_name", "KINETIC")
        tagline = brand_identity.get("tagline", "Fueling the Next Aesthetic")
        
        return {
            "narrative_structure": "A linear immersive narrative showcasing high-status design value, following with feature items and key CTA.",
            "sections": [
                {
                    "id": "hero-01",
                    "type": "hero",
                    "title": name,
                    "description": "Immersive landing hero.",
                    "content_data": {
                        "heading": tagline,
                        "subheading": brand_identity.get("brand_narrative", ""),
                        "primary_cta": {
                            "text": "Explore Collection" if not is_turkish else "Koleksiyonu Keşfet",
                            "action": "#explore"
                        }
                    },
                    "visual_weight": 10,
                    "layout_preset": "full-viewport"
                },
                {
                    "id": "benefits-01",
                    "type": "benefits",
                    "title": "Core Values" if not is_turkish else "Temel Değerler",
                    "description": "Grid of core benefits.",
                    "content_data": {
                        "heading": "Engineered Perfection" if not is_turkish else "Kusursuz Mühendislik",
                        "items": [
                            {
                                "title": item.get("title", "Aesthetic Power"),
                                "description": item.get("description", "Premium look.")
                            } for item in brand_identity.get("key_benefits", [])
                        ]
                    },
                    "visual_weight": 7,
                    "layout_preset": "grid-asymmetric"
                },
                {
                    "id": "footer-01",
                    "type": "footer",
                    "title": "Footer",
                    "description": "Minimal closing brand representation.",
                    "content_data": {
                        "heading": name,
                        "subheading": "© 2026. All rights reserved."
                    },
                    "visual_weight": 4,
                    "layout_preset": "simple-stack"
                }
            ]
        }

if __name__ == "__main__":
    sample_tokens = {"prompt_hint": "Modern tech studio"}
    sample_brand = {"brand_name": "NEXUS", "tagline": "Next-Gen AI"}
    sample_visual = {"color_tokens": {"background": "#000"}}
    print(json.dumps(execute_ux_architect(sample_tokens, sample_brand, sample_visual), indent=2, ensure_ascii=False))
