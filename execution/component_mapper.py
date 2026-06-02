import os
import json
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

def get_directive() -> str:
    """Reads the frontend-arch directive."""
    directive_path = Path(__file__).parent.parent / "directives" / "frontend-arch.md"
    if not directive_path.exists():
        raise FileNotFoundError("Directive frontend-arch not found.")
    return directive_path.read_text(encoding="utf-8")

def execute_component_mapper(enriched_tokens: dict, visual_language: dict, experience_flow: dict, motion_graph: dict, model: str = "anthropic/claude-3-haiku") -> dict:
    """
    Executes the Component Mapper (Frontend Architect) agent, resolving concrete component items and CSS variables setup.
    """
    print(f"[API CALL] Component Mapper resolving component registry mapping using {model}...")
    
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=OPENROUTER_API_KEY,
    )
    
    # Search Qdrant RAG components
    rag_components = []
    try:
        from execution.qdrant_manager import search_components
        brand_name = enriched_tokens.get("brand", {}).get("name", "")
        emotion_name = enriched_tokens.get("emotion", {}).get("name", "")
        spatial_mode = enriched_tokens.get("spatial", {}).get("mode_name", "")
        prompt_hint = enriched_tokens.get("metadata", {}).get("session_prompt", "")
        search_query = f"brand archetype: {brand_name}, emotion: {emotion_name}, layout spatial mode: {spatial_mode}, original user prompt: {prompt_hint}"
        
        print(f"[RAG] Querying Qdrant for semantic components with: '{search_query[:80]}...'")
        rag_components = search_components(search_query, limit=8)
    except Exception as e:
        print(f"[RAG WARNING] Failed to query Qdrant RAG: {e}. Falling back to default.")

    rag_components_text = ""
    if rag_components:
        print(f"[RAG SUCCESS] Retrieved {len(rag_components)} semantic components from Qdrant.")
        rag_components_text = "\n### SEMANTICALLY RETRIEVED COMPONENTS (PREFER AND MAP THESE ID'S):\n"
        for comp in rag_components:
            rag_components_text += f"- Component ID: {comp['id']}\n"
            rag_components_text += f"  Name: {comp['name']}\n"
            rag_components_text += f"  Description: {comp['description']}\n"
            rag_components_text += f"  Emotions: {', '.join(comp['emotions'])}\n"
            rag_components_text += f"  Archetypes: {', '.join(comp['archetypes'])}\n\n"
            
    system_prompt = get_directive()
    
    user_content = f"Resolved Design Tokens:\n{json.dumps(enriched_tokens, indent=2)}\n\n"
    user_content += f"Visual Language Style:\n{json.dumps(visual_language, indent=2)}\n\n"
    user_content += f"Experience Flow (Layout Sections):\n{json.dumps(experience_flow, indent=2)}\n\n"
    user_content += f"Motion Graph:\n{json.dumps(motion_graph, indent=2)}\n\n"
    if rag_components_text:
        user_content += rag_components_text + "\n"
    user_content += "Generate the Component Plan JSON. Remember to output ONLY valid JSON, with NO other text or explanation."
    
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
        component_plan = json.loads(raw_output.strip())
        
        # Inject dynamic JSX code from Qdrant into the plan if matching
        if rag_components and "mapped_components" in component_plan:
            for mapped in component_plan["mapped_components"]:
                comp_id = mapped.get("component_id")
                matching_rag = next((c for c in rag_components if c["id"] == comp_id), None)
                if matching_rag:
                    mapped["jsx_code"] = matching_rag["jsx_code"]
                    mapped["is_dynamic_rag"] = True
                    
        return component_plan
    except json.JSONDecodeError as e:
        print(f"[ERROR] Component Mapper outputted invalid JSON: {e}")
        print(f"Raw Output:\n{raw_output}")
        # Fallback template
        colors = visual_language.get("color_tokens", {})
        typo = visual_language.get("typography_tokens", {})
        ui = visual_language.get("ui_tokens", {})
        
        css_vars = f"""
:root {{
  --font-header: '{typo.get("header_font", "Playfair Display")}', serif; 
  --font-body: '{typo.get("body_font", "Inter")}', sans-serif;
  --color-bg: {colors.get("background", "#000000")};
  --color-fg: {colors.get("foreground", "#FFFFFF")};
  --color-accent: {colors.get("primary_accent", "#D4AF37")};
  --color-muted: {colors.get("muted", "#A8A8A8")};
  --border-color: {colors.get("border", "rgba(255,255,255,0.08)")};
  --card-bg: {colors.get("card_background", "rgba(255,255,255,0.03)")};
  --border-radius: {ui.get("border_radius", "12px")};
  --border-width: {ui.get("border_width", "1px")};
}}
"""
        mapped = []
        for sec in experience_flow.get("sections", []):
            sec_type = sec.get("type", "")
            comp_id = "FeatureGrid"
            if sec_type == "hero":
                comp_id = "ImmersiveHero"
            elif sec_type == "marquee":
                comp_id = "Marquee"
            elif sec_type == "bento-showcase":
                comp_id = "BentoGrid"
            elif sec_type == "parallax-gallery":
                comp_id = "ParallaxGallery"
            elif sec_type == "text-reveal":
                comp_id = "TextReveal"
            elif sec_type == "testimonials":
                comp_id = "TestimonialCarousel"
            elif sec_type == "stats":
                comp_id = "StatsCounter"
            elif sec_type == "pin-section":
                comp_id = "ScrollPinSection"
            elif sec_type == "gallery":
                comp_id = "InteractiveGallery"
            elif sec_type == "cta":
                comp_id = "MotionCTA"
            elif sec_type == "footer":
                comp_id = "GlassmorphicFooter"
                
            mapped.append({
                "section_id": sec.get("id"),
                "component_id": comp_id,
                "variants": "default",
                "resolved_props": {
                    "title": sec.get("title"),
                    "subtitle": sec.get("description"),
                    "heading": sec.get("content_data", {}).get("heading", ""),
                    "subheading": sec.get("content_data", {}).get("subheading", ""),
                    "items": sec.get("content_data", {}).get("items", []),
                    "primary_cta": sec.get("content_data", {}).get("primary_cta", {})
                },
                "motion_config": {
                    "preset": "fade_in_up",
                    "duration": 0.8
                },
                "a11y_notes": "Use high contrast colors and semantic tags."
            })
            
        return {
            "global_styles": {
                "fonts_import": f"https://fonts.googleapis.com/css2?family={typo.get('header_font', 'Playfair+Display').replace(' ', '+')}&family={typo.get('body_font', 'Inter').replace(' ', '+')}&display=swap",
                "css_vars": css_vars.strip()
            },
            "mapped_components": mapped
        }

if __name__ == "__main__":
    sample_tokens = {}
    sample_visual = {"color_tokens": {"background": "#000", "foreground": "#fff"}, "typography_tokens": {"header_font": "Satoshi", "body_font": "Inter"}}
    sample_flow = {"sections": [{"id": "hero-01", "type": "hero", "title": "Brand"}]}
    sample_motion = {}
    print(json.dumps(execute_component_mapper(sample_tokens, sample_visual, sample_flow, sample_motion), indent=2, ensure_ascii=False))
