# -*- coding: utf-8 -*-
"""
ANDIP Vision-First Orchestrator Pipeline.
This module executes the 5-stage Vision-First Pipeline sequentially:
1. Moodboard Generation & Analysis -> enriched_dna (Design DNA)
2. Design Spec Sheet Generation & Analysis -> visual_language (Style Guide tokens)
3. Wireframe Generation & Analysis -> experience_flow (Layout & UX structure)
4. Component Renders & Analysis -> component_plan (Visual Specs & Assets)
5. Motion Storyboard Generation & Analysis -> motion_graph (Curves & Easing)

No caching allowed for visual generation to guarantee unique creative outputs.
Strict failure: If any step fails, it throws an error immediately instead of falling back silently.
"""

import os
import json
import uuid
import sys
import traceback
from pathlib import Path
from dotenv import load_dotenv

# Import Phase 1 Core wrappers
from execution.image_generator import generate_image
from execution.vision_analyzer import analyze_image

# Import existing text-based agents for combined hybrid orchestration
from execution.brand_strategist import execute_brand_strategist
from execution.art_director import execute_art_director
from execution.ux_architect import execute_ux_architect
from execution.motion_director import execute_motion_director
from execution.component_mapper import execute_component_mapper
from execution.critic import execute_critic

# Import ontology resolver
from execution.ontology_engine import resolve_design_dna

# Import our brand new Phase 2 prompt templates
import execution.visual_stage_prompts as prompts

load_dotenv()

BASE_DIR = Path(__file__).parent.parent
TMP_DIR = BASE_DIR / ".tmp"

def run_vision_pipeline(prompt: str, session_id: str = None) -> dict:
    """
    Orchestrates the complete 5-stage Vision-First Pipeline.
    Strictly raises exceptions on failure to ensure the strict failure contract.
    """
    if not session_id:
        session_id = f"sess_{uuid.uuid4().hex[:12]}"
        
    session_dir = TMP_DIR / "pipeline" / session_id
    visuals_dir = session_dir / "visuals"
    
    # Ensure directories exist
    visuals_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"\n==================================================")
    print(f"[VISION PIPELINE START] INITIALIZING VISION-FIRST FLOW")
    print(f"Prompt: '{prompt}'")
    print(f"Session: {session_id}")
    print(f"==================================================\n")
    
    session_log = {
        "metadata": {
            "session_id": session_id,
            "prompt": prompt,
            "pipeline_type": "vision_first",
            "warnings": [],
            "corrections": []
        },
        "steps": {},
        "visual_assets": {}
    }
    
    try:
        # ----------------------------------------------------
        # STAGE 1: MOODBOARD
        # ----------------------------------------------------
        print("\n--- [STAGE 1/5] MOODBOARD GENERATION & DNA EXTRACTION ---")
        moodboard_img_path = visuals_dir / "stage_1_moodboard.png"
        moodboard_prompt = prompts.MOODBOARD_GENERATION.format(brand_concept=prompt)
        
        # 1. Generate visual moodboard
        generate_image(moodboard_prompt, moodboard_img_path)
        session_log["visual_assets"]["moodboard"] = str(moodboard_img_path.relative_to(BASE_DIR))
        
        # 2. Analyze using Vision AI
        vision_dna = analyze_image(moodboard_img_path, prompts.MOODBOARD_ANALYSIS)
        
        # 3. Resolve & enrich DNA using our local design ontology database
        print("[STAGE 1] Enriching design DNA with local ontology database...")
        # Prepare input for local ontology engine
        dna_input = {
            "core_emotion": vision_dna.get("emotion", {}).get("primary", "luxury"),
            "brand_archetype": vision_dna.get("brand", {}).get("archetype", "everyman"),
            "visual_density": vision_dna.get("emotion", {}).get("visual_density", "medium"),
            "motion_energy": vision_dna.get("emotion", {}).get("motion_energy", 5),
            "prompt_hint": prompt
        }
        enriched_dna = resolve_design_dna(dna_input)
        
        # Capture warning/correction metadata
        session_log["metadata"]["warnings"].extend(enriched_dna["metadata"].get("applied_warnings", []))
        session_log["metadata"]["corrections"].extend(enriched_dna["metadata"].get("applied_corrections", []))
        
        # Override local values with EXACT vision-extracted assets for high fidelity
        enriched_dna["brand"]["name"] = vision_dna.get("brand", {}).get("name", enriched_dna["brand"]["name"])
        enriched_dna["colors"]["background"] = vision_dna.get("colors", {}).get("background", enriched_dna["colors"]["background"])
        enriched_dna["colors"]["foreground"] = vision_dna.get("colors", {}).get("foreground", enriched_dna["colors"]["foreground"])
        enriched_dna["colors"]["accent"] = vision_dna.get("colors", {}).get("accent", enriched_dna["colors"]["accent"])
        enriched_dna["colors"]["muted"] = vision_dna.get("colors", {}).get("muted", enriched_dna["colors"]["muted"])
        
        enriched_dna["typography"]["header_font"] = vision_dna.get("typography", {}).get("header_font_suggestion", enriched_dna["typography"]["header_font"])
        enriched_dna["typography"]["body_font"] = vision_dna.get("typography", {}).get("body_font_suggestion", enriched_dna["typography"]["body_font"])
        
        # Add visual reference references to DNA
        enriched_dna["visual_reference"] = session_log["visual_assets"]["moodboard"]
        
        # Save Step 1 output
        session_log["steps"]["step_1_discovery"] = enriched_dna
        (session_dir / "step_1_discovery.json").write_text(
            json.dumps(enriched_dna, indent=2, ensure_ascii=False), encoding="utf-8"
        )
        
        # ----------------------------------------------------
        # RUN BRAND STRATEGIST (Text agent using DNA context)
        # ----------------------------------------------------
        print("\n--- [HYBRID STEP] RUNNING BRAND STRATEGIST ---")
        brand_identity = execute_brand_strategist(enriched_dna)
        session_log["steps"]["step_2_brand_strategy"] = brand_identity
        (session_dir / "step_2_brand_strategy.json").write_text(
            json.dumps(brand_identity, indent=2, ensure_ascii=False), encoding="utf-8"
        )
        
        # ----------------------------------------------------
        # STAGE 2: DESIGN SPECS
        # ----------------------------------------------------
        print("\n--- [STAGE 2/5] DESIGN SPEC SHEET GENERATION & TOKEN EXTRACTION ---")
        spec_img_path = visuals_dir / "stage_2_design_spec.png"
        spec_prompt = prompts.DESIGN_SPECS_GENERATION.format(
            brand_concept=prompt,
            primary_emotion=enriched_dna["emotion"]["name"],
            bg_color=enriched_dna["colors"]["background"],
            fg_color=enriched_dna["colors"]["foreground"],
            accent_color=enriched_dna["colors"]["accent"],
            header_font=enriched_dna["typography"]["header_font"],
            body_font=enriched_dna["typography"]["body_font"]
        )
        
        # 1. Generate design specs image
        generate_image(spec_prompt, spec_img_path)
        session_log["visual_assets"]["design_spec"] = str(spec_img_path.relative_to(BASE_DIR))
        
        # 2. Extract precise token specifications using Vision AI
        visual_tokens = analyze_image(spec_img_path, prompts.DESIGN_SPECS_ANALYSIS)
        
        # 3. Create Art Director output merging text intelligence with precise visual specs
        print("[STAGE 2] Merging extracted design system specs into Visual Language...")
        visual_language = execute_art_director(enriched_dna, brand_identity)
        
        # Update colors with precise hex tokens from Design Spec
        if "colors" in visual_tokens:
            for color_key, val in visual_tokens["colors"].items():
                if val:
                    if color_key == "primary_accent" or color_key == "accent":
                        visual_language["color_tokens"]["primary_accent"] = val
                    elif color_key == "secondary_accent":
                        visual_language["color_tokens"]["secondary_accent"] = val
                    else:
                        visual_language["color_tokens"][color_key] = val
                        
        # Update typography family suggestions
        if "typography" in visual_tokens:
            typo_data = visual_tokens["typography"]
            visual_language["typography_tokens"]["header_font"] = typo_data.get("header_font", visual_language["typography_tokens"]["header_font"])
            visual_language["typography_tokens"]["body_font"] = typo_data.get("body_font", visual_language["typography_tokens"]["body_font"])
            if "font_sizes" in typo_data:
                visual_language["typography_tokens"]["font_sizes"] = typo_data["font_sizes"]
            if "font_weights" in typo_data:
                visual_language["typography_tokens"]["font_weights"] = typo_data["font_weights"]
                
        # Update spacing and border radius
        if "border_radius" in visual_tokens:
            visual_language["ui_tokens"]["border_radius_tokens"] = visual_tokens["border_radius"]
            # Set default standard radius
            visual_language["ui_tokens"]["border_radius"] = visual_tokens["border_radius"].get("md", "8px")
        if "shadows" in visual_tokens:
            visual_language["ui_tokens"]["shadow_tokens"] = visual_tokens["shadows"]
            visual_language["ui_tokens"]["box_shadow"] = visual_tokens["shadows"].get("md", "")
        if "spacing" in visual_tokens:
            visual_language["ui_tokens"]["spacing"] = visual_tokens["spacing"]
            
        visual_language["visual_reference"] = session_log["visual_assets"]["design_spec"]
        
        # Save Step 3 output
        session_log["steps"]["step_3_art_direction"] = visual_language
        (session_dir / "step_3_art_direction.json").write_text(
            json.dumps(visual_language, indent=2, ensure_ascii=False), encoding="utf-8"
        )
        
        # ----------------------------------------------------
        # STAGE 3: WIREFRAME
        # ----------------------------------------------------
        print("\n--- [STAGE 3/5] WIREFRAME GENERATION & LAYOUT ANALYSIS ---")
        wireframe_img_path = visuals_dir / "stage_3_wireframe.png"
        wireframe_prompt = prompts.WIREFRAME_GENERATION.format(
            brand_concept=prompt,
            primary_emotion=enriched_dna["emotion"]["name"],
            bg_color=visual_language["color_tokens"]["background"],
            accent_color=visual_language["color_tokens"]["primary_accent"],
            header_font=visual_language["typography_tokens"]["header_font"],
            body_font=visual_language["typography_tokens"]["body_font"]
        )
        
        # 1. Generate wireframe
        generate_image(wireframe_prompt, wireframe_img_path)
        session_log["visual_assets"]["wireframe"] = str(wireframe_img_path.relative_to(BASE_DIR))
        
        # 2. Extract layouts using Vision AI
        wireframe_flow = analyze_image(wireframe_img_path, prompts.WIREFRAME_ANALYSIS)
        
        # 3. Create UX Architecture merging structured section content details with visual layout
        print("[STAGE 3] Construction of immersive UX architecture based on visual layout...")
        ux_flow = execute_ux_architect(enriched_dna, brand_identity, visual_language)
        
        # Map wireframe structural sections into UX architect sections
        if "sections" in wireframe_flow and isinstance(wireframe_flow["sections"], list):
            print(f"[STAGE 3] Visual wireframe contains {len(wireframe_flow['sections'])} sections. Injecting layouts...")
            
            # Match wireframe sections with UX sections to merge layout shapes
            for idx, w_sec in enumerate(wireframe_flow["sections"]):
                w_type = w_sec.get("type", "").lower()
                # Find matching UX section by type or order
                ux_sec = None
                if idx < len(ux_flow.get("sections", [])):
                    ux_sec = ux_flow["sections"][idx]
                else:
                    # Search matching by type
                    ux_sec = next((s for s in ux_flow.get("sections", []) if s.get("type", "").lower() == w_type), None)
                    
                if ux_sec:
                    ux_sec["visual_weight"] = w_sec.get("visual_weight", ux_sec.get("visual_weight", 5))
                    ux_sec["layout_preset"] = w_sec.get("layout_grid_type", ux_sec.get("layout_preset", "asymmetric-grid"))
                    ux_sec["layout_description"] = w_sec.get("layout_description", "")
                    ux_sec["wireframe_content_hints"] = w_sec.get("content_elements", [])
                    ux_sec["suggested_alignment"] = w_sec.get("suggested_alignment", "left")
            
            # Save global layout type
            ux_flow["global_layout_grid_type"] = wireframe_flow.get("layout_grid_type", "asymmetric")
            
        ux_flow["visual_reference"] = session_log["visual_assets"]["wireframe"]
        
        # Save Step 4 output
        session_log["steps"]["step_4_ux_architecture"] = ux_flow
        (session_dir / "step_4_ux_architecture.json").write_text(
            json.dumps(ux_flow, indent=2, ensure_ascii=False), encoding="utf-8"
        )
        
        # ----------------------------------------------------
        # STAGE 4: COMPONENT DETAILS
        # ----------------------------------------------------
        print("\n--- [STAGE 4/5] COMPONENT DETAIL RENDER GENERATION & STRUCTURING ---")
        
        # Identify top / primary components to render (typically the Hero section is critical)
        sections = ux_flow.get("sections", [])
        hero_sec = next((s for s in sections if s.get("type") == "hero"), None)
        if not hero_sec and sections:
            hero_sec = sections[0]
            
        comp_id = hero_sec.get("id", "hero-01") if hero_sec else "hero-01"
        comp_type = hero_sec.get("type", "hero") if hero_sec else "hero"
        
        comp_img_path = visuals_dir / f"stage_4_{comp_id}_component.png"
        comp_prompt = prompts.COMPONENT_GENERATION.format(
            component_type=comp_type.upper(),
            visual_style_description=hero_sec.get("layout_description", "premium bento-grid dynamic layout") if hero_sec else "premium",
            bg_color=visual_language["color_tokens"]["background"],
            accent_color=visual_language["color_tokens"]["primary_accent"],
            muted_color=visual_language["color_tokens"]["muted"],
            header_font=visual_language["typography_tokens"]["header_font"],
            body_font=visual_language["typography_tokens"]["body_font"]
        )
        
        # 1. Generate high-fidelity component render
        generate_image(comp_prompt, comp_img_path)
        session_log["visual_assets"]["hero_component_render"] = str(comp_img_path.relative_to(BASE_DIR))
        
        # 2. Extract specific layout and hover micro-tokens using Vision AI
        comp_specs = analyze_image(comp_img_path, prompts.COMPONENT_ANALYSIS)
        
        # 3. Execute component mapper to construct full component registry
        # Motion graph mock or initial empty dict, as we compute it in Step 5
        print("[STAGE 4] Mapping component architecture and compiling registry...")
        component_plan = execute_component_mapper(enriched_dna, visual_language, ux_flow, {})
        
        # Inject exact vision reference details into mapped components
        if "mapped_components" in component_plan:
            for mapped in component_plan["mapped_components"]:
                m_type = mapped.get("component_id", "").lower()
                m_sec = mapped.get("section_id", "")
                
                # Check if it's the hero or primary component
                if m_sec == comp_id or "hero" in m_type:
                    print(f"[STAGE 4 SUCCESS] Injecting visual reference and specs into component: {mapped.get('component_id')}")
                    mapped["vision_reference_path"] = str(comp_img_path.absolute())
                    mapped["visual_specs"] = comp_specs
                    
        # Save Step 6 output
        session_log["steps"]["step_6_frontend_arch"] = component_plan
        (session_dir / "step_6_frontend_arch.json").write_text(
            json.dumps(component_plan, indent=2, ensure_ascii=False), encoding="utf-8"
        )
        
        # ----------------------------------------------------
        # STAGE 5: MOTION STORYBOARD
        # ----------------------------------------------------
        print("\n--- [STAGE 5/5] MOTION STORYBOARD GENERATION & PHYSICS EXTRACTION ---")
        storyboard_img_path = visuals_dir / "stage_5_motion_storyboard.png"
        
        section_ids = [s.get("id") for s in sections]
        storyboard_prompt = prompts.MOTION_STORYBOARD_GENERATION.format(
            brand_concept=prompt,
            primary_emotion=enriched_dna["emotion"]["name"],
            accent_color=visual_language["color_tokens"]["primary_accent"],
            sections_list=", ".join(section_ids)
        )
        
        # 1. Generate storyboard image
        generate_image(storyboard_prompt, storyboard_img_path)
        session_log["visual_assets"]["motion_storyboard"] = str(storyboard_img_path.relative_to(BASE_DIR))
        
        # 2. Extract precise curves using Vision AI
        motion_tokens = analyze_image(storyboard_img_path, prompts.MOTION_STORYBOARD_ANALYSIS)
        
        # 3. Create Motion Direction configuration merging visual timing specs
        print("[STAGE 5] Creating Motion Graph and physics configurations...")
        motion_graph = execute_motion_director(enriched_dna, visual_language, ux_flow)
        
        # Inject precise easing cubic-bezier or springs extracted from storyboard
        if motion_tokens:
            print(f"[STAGE 5 SUCCESS] Injecting storyboard curves into Motion Graph: {motion_tokens.get('easing_curve')}")
            motion_graph["visual_motion_physics"] = motion_tokens
            
            # Apply to global and section configurations
            motion_graph["global_motion"]["easing_curve"] = motion_tokens.get("easing_curve")
            motion_graph["global_motion"]["pacing_feel"] = motion_tokens.get("pacing_feel")
            motion_graph["global_motion"]["duration"] = motion_tokens.get("duration")
            
            # Apply to individual section entries
            for anim in motion_graph.get("section_animations", []):
                if anim.get("section_id") == comp_id: # Primary hero animated
                    anim["framer_motion_config"]["ease"] = motion_tokens.get("easing_curve")
                    anim["framer_motion_config"]["duration"] = motion_tokens.get("duration")
                    if "initial_state" in motion_tokens:
                        anim["framer_motion_config"]["initial"] = motion_tokens["initial_state"]
                    if "final_state" in motion_tokens:
                        anim["framer_motion_config"]["animate"] = motion_tokens["final_state"]
                        
        motion_graph["visual_reference"] = session_log["visual_assets"]["motion_storyboard"]
        
        # Save Step 5 output
        session_log["steps"]["step_5_motion_direction"] = motion_graph
        (session_dir / "step_5_motion_direction.json").write_text(
            json.dumps(motion_graph, indent=2, ensure_ascii=False), encoding="utf-8"
        )
        
        # ----------------------------------------------------
        # RUN CRITIC AUDIT
        # ----------------------------------------------------
        print("\n--- [CRITIC AUDIT] RUNNING COGNITIVE AUDIT GATE ---")
        full_session_data = {
            "dna": enriched_dna,
            "brand_identity": brand_identity,
            "visual_language": visual_language,
            "experience_flow": ux_flow,
            "motion_graph": motion_graph,
            "component_plan": component_plan
        }
        critic_report = execute_critic(full_session_data)
        session_log["steps"]["step_7_critic"] = critic_report
        (session_dir / "step_7_critic.json").write_text(
            json.dumps(critic_report, indent=2, ensure_ascii=False), encoding="utf-8"
        )
        
        # ----------------------------------------------------
        # ASSEMBLE FINAL BLUEPRINT JSON
        # ----------------------------------------------------
        print("\n[VISION PIPELINE SUCCESS] Assembling final Experience Blueprint...")
        experience_blueprint = {
            "metadata": session_log["metadata"],
            "design_dna": enriched_dna,
            "brand_identity": brand_identity,
            "visual_language": visual_language,
            "experience_flow": ux_flow,
            "motion_graph": motion_graph,
            "component_plan": component_plan,
            "critique_report": critic_report,
            "visual_assets": session_log["visual_assets"]
        }
        
        # Save to session directory
        (session_dir / "experience_blueprint.json").write_text(
            json.dumps(experience_blueprint, indent=2, ensure_ascii=False), encoding="utf-8"
        )
        
        # Save to prompt cache directory
        (TMP_DIR / "cache").mkdir(parents=True, exist_ok=True)
        import hashlib
        prompt_hash = hashlib.md5(prompt.encode("utf-8")).hexdigest()
        cache_file = TMP_DIR / "cache" / f"blueprint_{prompt_hash}.json"
        cache_file.write_text(
            json.dumps(experience_blueprint, indent=2, ensure_ascii=False), encoding="utf-8"
        )
        
        print(f"\n[SUCCESS] VISION-FIRST PIPELINE RUN FINISHED!")
        print(f"Experience Blueprint saved at: {session_dir / 'experience_blueprint.json'}")
        print(f"==================================================\n")
        
        return experience_blueprint
        
    except Exception as e:
        print(f"\n[VISION PIPELINE CRITICAL ERROR] Pipeline failed on visual workflow: {e}")
        traceback.print_exc()
        # Strict failure: Raise exception directly instead of silently falling back to text-only.
        raise RuntimeError(f"Vision-First pipeline execution failed. Details: {e}")

if __name__ == "__main__":
    test_prompt = "Futuristic neon glowing cyber-fashion landing page."
    if len(sys.argv) > 1:
        test_prompt = sys.argv[1]
    run_vision_pipeline(test_prompt)
