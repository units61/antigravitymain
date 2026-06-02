# -*- coding: utf-8 -*-
"""
ANDIP Vision-First Pipeline V2: 2-Stage Hybrid Orchestrator.
Consolidates 5 stages into 2 mega-stages:
  Stage A: Design Blueprint (Moodboard + Design Spec + Wireframe) -> enriched_dna + visual_language + ux_flow
  Stage B: Motion & Interaction (Hero Component + Motion Storyboard) -> component_plan + motion_graph

Same output format (experience_blueprint.json) for downstream compatibility.
"""

import os
import json
import uuid
import sys
import hashlib
import traceback
from pathlib import Path
from dotenv import load_dotenv

# Core wrappers
from execution.image_generator import generate_image
from execution.vision_analyzer import analyze_image

# Text-based agents (unchanged)
from execution.brand_strategist import execute_brand_strategist
from execution.art_director import execute_art_director
from execution.ux_architect import execute_ux_architect
from execution.motion_director import execute_motion_director
from execution.component_mapper import execute_component_mapper
from execution.critic import execute_critic

# Ontology resolver
from execution.ontology_engine import resolve_design_dna

# V2 prompt templates
import execution.visual_stage_prompts_v2 as prompts_v2

load_dotenv()

BASE_DIR = Path(__file__).parent.parent
TMP_DIR = BASE_DIR / ".tmp"


def run_vision_pipeline_v2(prompt: str, session_id: str = None) -> dict:
    """
    Orchestrates the 2-stage Vision-First Pipeline V2.
    Stage A: Design Blueprint -> DNA + Tokens + Layout
    Stage B: Motion & Interaction -> Component specs + Motion physics
    """
    if not session_id:
        session_id = f"sess_v2_{uuid.uuid4().hex[:12]}"

    session_dir = TMP_DIR / "pipeline" / session_id
    visuals_dir = session_dir / "visuals"
    visuals_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n{'='*60}")
    print(f"[VISION PIPELINE V2] 2-STAGE HYBRID FLOW")
    print(f"Prompt: '{prompt}'")
    print(f"Session: {session_id}")
    print(f"{'='*60}\n")

    session_log = {
        "metadata": {
            "session_id": session_id,
            "prompt": prompt,
            "pipeline_type": "vision_first_v2_hybrid",
            "pipeline_version": "2.0",
            "warnings": [],
            "corrections": []
        },
        "steps": {},
        "visual_assets": {}
    }

    try:
        # ============================================================
        # STAGE A: DESIGN BLUEPRINT
        # (Moodboard + Design Spec + Wireframe in ONE image)
        # ============================================================
        print("\n--- [STAGE A] DESIGN BLUEPRINT GENERATION & ANALYSIS ---")
        print("[STAGE A] Generating combined Moodboard + Design Spec + Wireframe...")

        blueprint_img_path = visuals_dir / "stage_a_design_blueprint.png"
        blueprint_prompt = prompts_v2.STAGE_A_GENERATION.format(brand_concept=prompt)

        # 1. Generate the combined design blueprint image
        generate_image(blueprint_prompt, blueprint_img_path)
        session_log["visual_assets"]["design_blueprint"] = str(blueprint_img_path.relative_to(BASE_DIR))

        # 2. Analyze using Vision AI — extract ALL specs from one image
        print("[STAGE A] Extracting DNA + Tokens + Layout from blueprint...")
        blueprint_data = analyze_image(blueprint_img_path, prompts_v2.STAGE_A_ANALYSIS)

        # 3. Resolve & enrich DNA using local ontology database
        print("[STAGE A] Enriching design DNA with local ontology database...")
        dna_input = {
            "core_emotion": blueprint_data.get("emotion", {}).get("primary", "vibrant"),
            "brand_archetype": blueprint_data.get("brand", {}).get("archetype", "creator"),
            "visual_density": blueprint_data.get("spatial", {}).get("density", "airy"),
            "motion_energy": blueprint_data.get("emotion", {}).get("motion_energy", 6),
            "prompt_hint": prompt
        }
        enriched_dna = resolve_design_dna(dna_input)

        # Capture metadata
        session_log["metadata"]["warnings"].extend(enriched_dna["metadata"].get("applied_warnings", []))
        session_log["metadata"]["corrections"].extend(enriched_dna["metadata"].get("applied_corrections", []))

        # Override with EXACT vision-extracted values for high fidelity
        enriched_dna["brand"]["name"] = blueprint_data.get("brand", {}).get("name", enriched_dna["brand"]["name"])
        enriched_dna["colors"]["background"] = blueprint_data.get("colors", {}).get("background", enriched_dna["colors"]["background"])
        enriched_dna["colors"]["foreground"] = blueprint_data.get("colors", {}).get("foreground", enriched_dna["colors"]["foreground"])
        enriched_dna["colors"]["accent"] = blueprint_data.get("colors", {}).get("accent", enriched_dna["colors"]["accent"])
        enriched_dna["colors"]["muted"] = blueprint_data.get("colors", {}).get("muted", enriched_dna["colors"]["muted"])
        enriched_dna["typography"]["header_font"] = blueprint_data.get("typography", {}).get("header_font", enriched_dna["typography"]["header_font"])
        enriched_dna["typography"]["body_font"] = blueprint_data.get("typography", {}).get("body_font", enriched_dna["typography"]["body_font"])
        enriched_dna["visual_reference"] = session_log["visual_assets"]["design_blueprint"]

        # Save Step 1
        session_log["steps"]["step_1_discovery"] = enriched_dna
        (session_dir / "step_1_discovery.json").write_text(
            json.dumps(enriched_dna, indent=2, ensure_ascii=False), encoding="utf-8"
        )

        # ============================================================
        # HYBRID: Brand Strategist (text agent)
        # ============================================================
        print("\n--- [HYBRID] RUNNING BRAND STRATEGIST ---")
        brand_identity = execute_brand_strategist(enriched_dna)
        session_log["steps"]["step_2_brand_strategy"] = brand_identity
        (session_dir / "step_2_brand_strategy.json").write_text(
            json.dumps(brand_identity, indent=2, ensure_ascii=False), encoding="utf-8"
        )

        # ============================================================
        # HYBRID: Art Director (text agent, enriched with visual tokens)
        # ============================================================
        print("\n--- [HYBRID] RUNNING ART DIRECTOR ---")
        visual_language = execute_art_director(enriched_dna, brand_identity)

        # Inject precise tokens extracted from the blueprint image
        if "colors" in blueprint_data:
            for key, val in blueprint_data["colors"].items():
                if val:
                    if key in ("accent", "primary_accent"):
                        visual_language["color_tokens"]["primary_accent"] = val
                    elif key == "secondary_accent":
                        visual_language["color_tokens"]["secondary_accent"] = val
                    else:
                        visual_language["color_tokens"][key] = val

        if "typography" in blueprint_data:
            typo = blueprint_data["typography"]
            visual_language["typography_tokens"]["header_font"] = typo.get("header_font", visual_language["typography_tokens"]["header_font"])
            visual_language["typography_tokens"]["body_font"] = typo.get("body_font", visual_language["typography_tokens"]["body_font"])
            if "font_sizes" in typo:
                visual_language["typography_tokens"]["font_sizes"] = typo["font_sizes"]
            if "font_weights" in typo:
                visual_language["typography_tokens"]["font_weights"] = typo["font_weights"]

        if "border_radius" in blueprint_data:
            visual_language["ui_tokens"]["border_radius_tokens"] = blueprint_data["border_radius"]
            visual_language["ui_tokens"]["border_radius"] = blueprint_data["border_radius"].get("md", "8px")
        if "shadows" in blueprint_data:
            visual_language["ui_tokens"]["shadow_tokens"] = blueprint_data["shadows"]
            visual_language["ui_tokens"]["box_shadow"] = blueprint_data["shadows"].get("md", "")
        if "spacing" in blueprint_data:
            visual_language["ui_tokens"]["spacing"] = blueprint_data["spacing"]

        visual_language["visual_reference"] = session_log["visual_assets"]["design_blueprint"]

        session_log["steps"]["step_3_art_direction"] = visual_language
        (session_dir / "step_3_art_direction.json").write_text(
            json.dumps(visual_language, indent=2, ensure_ascii=False), encoding="utf-8"
        )

        # ============================================================
        # HYBRID: UX Architect (text agent, enriched with wireframe layout)
        # ============================================================
        print("\n--- [HYBRID] RUNNING UX ARCHITECT ---")
        ux_flow = execute_ux_architect(enriched_dna, brand_identity, visual_language)

        # Inject wireframe sections from the blueprint analysis
        wireframe = blueprint_data.get("wireframe", {})
        if "sections" in wireframe and isinstance(wireframe["sections"], list):
            print(f"[STAGE A] Blueprint wireframe contains {len(wireframe['sections'])} sections. Injecting layouts...")

            for idx, w_sec in enumerate(wireframe["sections"]):
                w_type = w_sec.get("type", "").lower()
                ux_sec = None
                if idx < len(ux_flow.get("sections", [])):
                    ux_sec = ux_flow["sections"][idx]
                else:
                    ux_sec = next((s for s in ux_flow.get("sections", []) if s.get("type", "").lower() == w_type), None)

                if ux_sec:
                    ux_sec["visual_weight"] = w_sec.get("visual_weight", ux_sec.get("visual_weight", 5))
                    ux_sec["layout_preset"] = wireframe.get("layout_grid_type", ux_sec.get("layout_preset", "editorial_story"))
                    ux_sec["layout_description"] = w_sec.get("layout_description", "")
                    ux_sec["wireframe_content_hints"] = w_sec.get("content_elements", [])
                    ux_sec["suggested_alignment"] = w_sec.get("suggested_alignment", "center")

            ux_flow["global_layout_grid_type"] = wireframe.get("layout_grid_type", "editorial_story")

        ux_flow["visual_reference"] = session_log["visual_assets"]["design_blueprint"]

        session_log["steps"]["step_4_ux_architecture"] = ux_flow
        (session_dir / "step_4_ux_architecture.json").write_text(
            json.dumps(ux_flow, indent=2, ensure_ascii=False), encoding="utf-8"
        )

        # ============================================================
        # STAGE B: MOTION & INTERACTION
        # (Hero Component + Motion Storyboard in ONE image)
        # ============================================================
        print("\n--- [STAGE B] MOTION & INTERACTION GENERATION & ANALYSIS ---")

        sections = ux_flow.get("sections", [])
        hero_sec = next((s for s in sections if s.get("type") == "hero"), None)
        if not hero_sec and sections:
            hero_sec = sections[0]

        section_ids = [s.get("id", f"section_{i}") for i, s in enumerate(sections)]

        # Determine secondary accent color
        secondary_accent = visual_language["color_tokens"].get(
            "secondary_accent",
            visual_language["color_tokens"].get("muted", "#888888")
        )

        motion_img_path = visuals_dir / "stage_b_motion_interaction.png"
        motion_prompt = prompts_v2.STAGE_B_GENERATION.format(
            brand_concept=prompt,
            visual_style_description=hero_sec.get("layout_description", "editorial storytelling hero") if hero_sec else "editorial",
            bg_color=visual_language["color_tokens"]["background"],
            accent_color=visual_language["color_tokens"]["primary_accent"],
            secondary_accent=secondary_accent,
            header_font=visual_language["typography_tokens"]["header_font"],
            body_font=visual_language["typography_tokens"]["body_font"],
            sections_list=", ".join(section_ids)
        )

        # 1. Generate the combined motion & interaction image
        print("[STAGE B] Generating Hero Component + Motion Storyboard...")
        generate_image(motion_prompt, motion_img_path)
        session_log["visual_assets"]["motion_interaction"] = str(motion_img_path.relative_to(BASE_DIR))

        # 2. Analyze — extract hero specs + motion physics
        print("[STAGE B] Extracting component specs + animation physics...")
        motion_data = analyze_image(motion_img_path, prompts_v2.STAGE_B_ANALYSIS)

        # 3. Build component plan using component mapper (text agent)
        print("[STAGE B] Mapping component architecture...")
        component_plan = execute_component_mapper(enriched_dna, visual_language, ux_flow, {})

        # Inject hero visual specs from Stage B
        hero_specs = motion_data.get("hero_component", {})
        if "mapped_components" in component_plan and hero_specs:
            for mapped in component_plan["mapped_components"]:
                m_type = mapped.get("component_id", "").lower()
                if "hero" in m_type:
                    print(f"[STAGE B] Injecting hero visual specs into: {mapped.get('component_id')}")
                    mapped["vision_reference_path"] = str(motion_img_path.absolute())
                    mapped["visual_specs"] = hero_specs

        session_log["steps"]["step_6_frontend_arch"] = component_plan
        (session_dir / "step_6_frontend_arch.json").write_text(
            json.dumps(component_plan, indent=2, ensure_ascii=False), encoding="utf-8"
        )

        # 4. Build motion graph using motion director (text agent)
        print("[STAGE B] Creating Motion Graph and physics configurations...")
        motion_graph = execute_motion_director(enriched_dna, visual_language, ux_flow)

        # Inject precise motion physics from Stage B analysis
        motion_physics = motion_data.get("motion", {})
        if motion_physics:
            print(f"[STAGE B] Injecting motion physics: {motion_physics.get('easing_curve')}")
            motion_graph["visual_motion_physics"] = motion_physics

            # Apply to global config
            motion_graph["global_motion"]["easing_curve"] = motion_physics.get("easing_curve")
            motion_graph["global_motion"]["pacing_feel"] = motion_physics.get("pacing_feel")
            motion_graph["global_motion"]["duration"] = motion_physics.get("duration")

            # Inject spring physics if present
            if "spring_physics" in motion_physics:
                motion_graph["global_motion"]["spring_physics"] = motion_physics["spring_physics"]

            # Inject parallax config if present
            if "parallax" in motion_physics:
                motion_graph["global_motion"]["parallax"] = motion_physics["parallax"]

            # Inject stagger config if present
            if "stagger" in motion_physics:
                motion_graph["global_motion"]["stagger"] = motion_physics["stagger"]

            # Apply to individual section animations
            for anim in motion_graph.get("section_animations", []):
                anim["framer_motion_config"]["ease"] = motion_physics.get("easing_curve")
                anim["framer_motion_config"]["duration"] = motion_physics.get("duration")
                if "initial_state" in motion_physics:
                    anim["framer_motion_config"]["initial"] = motion_physics["initial_state"]
                if "final_state" in motion_physics:
                    anim["framer_motion_config"]["animate"] = motion_physics["final_state"]

            # Inject section transitions if present
            if "section_transitions" in motion_physics:
                motion_graph["section_transitions"] = motion_physics["section_transitions"]

        motion_graph["visual_reference"] = session_log["visual_assets"]["motion_interaction"]

        session_log["steps"]["step_5_motion_direction"] = motion_graph
        (session_dir / "step_5_motion_direction.json").write_text(
            json.dumps(motion_graph, indent=2, ensure_ascii=False), encoding="utf-8"
        )

        # ============================================================
        # CRITIC AUDIT
        # ============================================================
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

        # ============================================================
        # ASSEMBLE FINAL BLUEPRINT
        # ============================================================
        print("\n[VISION PIPELINE V2] Assembling final Experience Blueprint...")
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

        # Save to cache
        (TMP_DIR / "cache").mkdir(parents=True, exist_ok=True)
        prompt_hash = hashlib.md5(prompt.encode("utf-8")).hexdigest()
        cache_file = TMP_DIR / "cache" / f"blueprint_v2_{prompt_hash}.json"
        cache_file.write_text(
            json.dumps(experience_blueprint, indent=2, ensure_ascii=False), encoding="utf-8"
        )

        print(f"\n[SUCCESS] VISION PIPELINE V2 COMPLETED!")
        print(f"Blueprint: {session_dir / 'experience_blueprint.json'}")
        print(f"Visual Assets: {list(session_log['visual_assets'].keys())}")
        print(f"{'='*60}\n")

        return experience_blueprint

    except Exception as e:
        print(f"\n[VISION PIPELINE V2 ERROR] Pipeline failed: {e}")
        traceback.print_exc()
        raise RuntimeError(f"Vision-First V2 pipeline failed. Details: {e}")


if __name__ == "__main__":
    test_prompt = "A premium creative agency storytelling landing page with vibrant colors and editorial feel."
    if len(sys.argv) > 1:
        test_prompt = sys.argv[1]
    run_vision_pipeline_v2(test_prompt)
