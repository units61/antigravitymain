import os
import json
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

def get_directive() -> str:
    """Reads the brand-strategy directive."""
    directive_path = Path(__file__).parent.parent / "directives" / "brand-strategy.md"
    if not directive_path.exists():
        directive_path = Path(__file__).parent.parent / "skills" / "brand-strategist" / "SKILL.md"
    if not directive_path.exists():
        raise FileNotFoundError("Directive brand-strategy not found.")
    return directive_path.read_text(encoding="utf-8")

def execute_brand_strategist(enriched_tokens: dict, critic_feedback: str = "", model: str = "anthropic/claude-3-haiku") -> dict:
    """
    Executes the Brand Strategist agent, taking design tokens and returning a Brand Identity.
    """
    print(f"[API CALL] Brand Strategist generating identity using {model}...")
    
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=OPENROUTER_API_KEY,
    )
    
    system_prompt = get_directive()
    
    user_content = f"Here are the resolved Design Tokens:\n{json.dumps(enriched_tokens, indent=2)}\n\n"
    if critic_feedback:
        user_content += f"CRITIC FEEDBACK FOR REVISION:\n{critic_feedback}\n\nPlease revise the brand strategy to resolve this feedback.\n\n"
    user_content += "Generate the Brand Identity JSON. Remember to output ONLY valid JSON, with NO other text or explanation."
    
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content}
        ]
    )
    
    raw_output = response.choices[0].message.content.strip()
    
    # Cleanup Markdown codeblocks
    if raw_output.startswith("```json"):
        raw_output = raw_output[7:]
    if raw_output.startswith("```"):
        raw_output = raw_output[3:]
    if raw_output.endswith("```"):
        raw_output = raw_output[:-3]
        
    try:
        brand_identity = json.loads(raw_output.strip())
        return brand_identity
    except json.JSONDecodeError as e:
        print(f"[ERROR] Brand Strategist outputted invalid JSON: {e}")
        print(f"Raw Output:\n{raw_output}")
        # Fallback template
        is_turkish = "turkish" in str(enriched_tokens).lower() or "sitem" in str(enriched_tokens).lower()
        return {
            "brand_name": "KINETIC" if not is_turkish else "SİNERJİ",
            "tagline": "Fueling the Next Aesthetic" if not is_turkish else "Geleceğin Estetiğini Şekillendiriyoruz",
            "brand_narrative": "A premium, forward-thinking digital experience designed to disrupt standard structures." if not is_turkish else "Standart yapıları bozmak için tasarlanmış, birinci sınıf, geleceğe yönelik bir dijital deneyim.",
            "voice_and_tone": {
                "attributes": ["Bold", "Disruptive", "Premium"],
                "do_rules": ["Use strong typography", "Emphasize whitespace"],
                "dont_rules": ["Do not use boring blue colors", "Avoid long blocks of text"]
            },
            "value_proposition": "The absolute pinnacle of style meets function.",
            "key_benefits": [
                {
                    "title": "Aesthetic Edge" if not is_turkish else "Estetik Güç",
                    "description": "Uniquely crafted visuals designed to capture and hold digital attention." if not is_turkish else "Dijital dikkati yakalamak ve elde tutmak için benzersiz şekilde tasarlanmış görseller."
                }
            ]
        }

if __name__ == "__main__":
    import sys
    # Dry run with sample tokens
    sample_tokens = {
        "brand": {"archetype": "rebel"},
        "emotion": {"id": "luxury", "visual_density": "low", "motion_energy": 6},
        "prompt_hint": "Luxury streetwear clothing shop"
    }
    print(json.dumps(execute_brand_strategist(sample_tokens), indent=2, ensure_ascii=False))
