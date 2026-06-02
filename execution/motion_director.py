import os
import json
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

def get_directive() -> str:
    """Reads the motion-direction directive."""
    directive_path = Path(__file__).parent.parent / "directives" / "motion-direction.md"
    if not directive_path.exists():
        raise FileNotFoundError("Directive motion-direction not found.")
    return directive_path.read_text(encoding="utf-8")

def execute_motion_director(enriched_tokens: dict, visual_language: dict, experience_flow: dict, model: str = "anthropic/claude-3-haiku") -> dict:
    """
    Executes the Motion Director agent, planning page scroll behavior, spring constant properties, and micro-interactions.
    """
    print(f"[API CALL] Motion Director constructing motion graph using {model}...")
    
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=OPENROUTER_API_KEY,
    )
    
    system_prompt = get_directive()
    
    user_content = f"Resolved Design Tokens:\n{json.dumps(enriched_tokens, indent=2)}\n\n"
    user_content += f"Visual Language Style:\n{json.dumps(visual_language, indent=2)}\n\n"
    user_content += f"Experience Flow (Layout Sections):\n{json.dumps(experience_flow, indent=2)}\n\n"
    user_content += "Generate the Motion Graph JSON. Remember to output ONLY valid JSON, with NO other text or explanation."
    
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
        motion_graph = json.loads(raw_output.strip())
        return motion_graph
    except json.JSONDecodeError as e:
        print(f"[ERROR] Motion Director outputted invalid JSON: {e}")
        print(f"Raw Output:\n{raw_output}")
        # Fallback template
        energy = enriched_tokens.get("emotion", {}).get("motion_energy", 5)
        stiffness = 100
        damping = 15
        
        if energy >= 7:
            stiffness = 180
            damping = 12
        elif energy <= 3:
            stiffness = 50
            damping = 25
            
        sections = experience_flow.get("sections", [])
        sec_anims = []
        for sec in sections:
            sec_anims.append({
                "section_id": sec.get("id", "section"),
                "scroll_trigger": True,
                "entrance_preset": "fade_in_up",
                "exit_preset": "none",
                "micro_interactions": {
                    "hover": "lift" if energy > 3 else "none",
                    "tap": "shrink" if energy > 3 else "none"
                },
                "framer_motion_config": {
                    "duration": 0.8 if energy <= 5 else 0.5,
                    "damping": damping,
                    "stiffness": stiffness
                }
            })
            
        return {
            "global_motion": {
                "page_transition": "fade",
                "scroll_behavior": "smooth",
                "lenis_options": {
                    "duration": 1.2,
                    "easing": "smooth"
                }
            },
            "gsap_config": {
                "smooth_scroll": True,
                "section_animations": [
                    {
                        "section_id": sec.get("id", "section"),
                        "pin": False,
                        "scrub": True,
                        "parallax_offset": 0.3,
                        "stagger_children": 0.12
                    } for sec in sections
                ]
            },
            "section_animations": sec_anims
        }

if __name__ == "__main__":
    sample_tokens = {"emotion": {"motion_energy": 8}}
    sample_visual = {}
    sample_flow = {"sections": [{"id": "hero"}, {"id": "features"}]}
    print(json.dumps(execute_motion_director(sample_tokens, sample_visual, sample_flow), indent=2, ensure_ascii=False))
