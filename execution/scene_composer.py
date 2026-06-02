import os
import json
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

def get_directive() -> str:
    """Reads the scene-composer directive."""
    directive_path = Path(__file__).parent.parent / "directives" / "scene-composer.md"
    if not directive_path.exists():
        raise FileNotFoundError("Directive scene-composer not found.")
    return directive_path.read_text(encoding="utf-8")

def execute_scene_composer(enriched_tokens: dict, story_scenes: dict, critic_feedback: str = "", model: str = "anthropic/claude-3.5-sonnet") -> dict:
    """
    Executes the Scene Composer agent, mapping story scenes to precise layout models, overlays, and depth settings.
    """
    # Safety check for model spelling typos
    if "claude-3-5" in model:
        model = "anthropic/claude-3.5-sonnet"
    print(f"[API CALL] Scene Composer mapping story to layout elements using {model}...")
    
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=OPENROUTER_API_KEY,
    )
    
    system_prompt = get_directive()
    
    user_content = f"Design DNA & Tokens:\n{json.dumps(enriched_tokens, indent=2)}\n\n"
    user_content += f"Story Scenes Storyboard:\n{json.dumps(story_scenes, indent=2)}\n\n"
    if critic_feedback:
        user_content += f"CRITIC FEEDBACK FOR REVISION:\n{critic_feedback}\n\nPlease adjust the composition to address this critique.\n\n"
    user_content += "Generate the Scene Mapping JSON. Remember to output ONLY valid JSON, with NO other text or explanation."
    
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content}
            ],
            temperature=0.3
        )
        
        raw_output = response.choices[0].message.content.strip()
        
        if raw_output.startswith("```json"):
            raw_output = raw_output[7:]
        if raw_output.startswith("```"):
            raw_output = raw_output[3:]
        if raw_output.endswith("```"):
            raw_output = raw_output[:-3]
            
        scene_mapping = json.loads(raw_output.strip())
        print("[SUCCESS] Scene composition maps successfully compiled by Composer AI!")
        return scene_mapping
    except Exception as e:
        print(f"[ERROR] Scene Composer failed: {e}. Executing robust fallback composition.")
        scenes = story_scenes.get("scenes", [])
        mapped_fallback = []
        
        layout_modes = ["fullscreen_canvas", "split_screen_narrative", "staggered_editorial", "bento_storyboard"]
        grammar_types = ["INTRODUCTION", "DISCOVERY", "REVEAL", "EXPLORATION", "PROOF", "TRANSFORMATION", "ACTION"]
        
        for idx, s in enumerate(scenes):
            g_type = grammar_types[idx % len(grammar_types)]
            l_mode = "fullscreen_canvas"
            if g_type in ["DISCOVERY", "EXPLORATION"]:
                l_mode = "split_screen_narrative"
            elif g_type == "PROOF":
                l_mode = "staggered_editorial"
                
            mapped_fallback.append({
                "scene_number": s.get("scene_number", idx + 1),
                "scene_name": s.get("name", f"Scene {idx + 1}"),
                "grammar_type": g_type,
                "layout_mode": l_mode,
                "depth_layering": {
                    "webgl_z_index": -1,
                    "content_z_index": 10,
                    "backdrop_blur_overlay": "backdrop-blur-[4px]" if l_mode == "split_screen_narrative" else "none"
                },
                "overlay_elements": {
                    "text_align": "center" if l_mode == "fullscreen_canvas" else "left",
                    "typography_role": "massive_kinetic_title" if idx == 0 else "dual_column_copy",
                    "copywriting_header": s.get("copywriting_header", "FALLBACK HEADER"),
                    "copywriting_body": s.get("copywriting_body", "Fallback description content.")
                },
                "required_react_interface_hooks": ["useScroll", "useTransform"]
            })
            
        return {"scenes_mapping": mapped_fallback}

if __name__ == "__main__":
    sample_tokens = {
        "brand": {"name": "Test Agency", "archetype": "creator"}
    }
    sample_story = {
        "scenes": [
            {"scene_number": 1, "name": "Awakening", "copywriting_header": "THE NEW AGE", "copywriting_body": "Design meets math."}
        ]
    }
    print(json.dumps(execute_scene_composer(sample_tokens, sample_story), indent=2, ensure_ascii=False))
