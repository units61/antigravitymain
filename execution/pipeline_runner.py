import os
import json
import uuid
import hashlib
from pathlib import Path
from dotenv import load_dotenv

# Import our agents
from execution.prompt_analyzer import analyze_prompt
from execution.ontology_engine import resolve_design_dna
from execution.brand_strategist import execute_brand_strategist
from execution.story_architect import execute_story_architect
from execution.art_director import execute_art_director
from execution.ux_architect import execute_ux_architect
from execution.scene_composer import execute_scene_composer
from execution.motion_director import execute_motion_director
from execution.experience_director import execute_experience_director
from execution.component_mapper import execute_component_mapper
from execution.critic import execute_critic

load_dotenv()

# Setup root paths
BASE_DIR = Path(__file__).parent.parent
TMP_DIR = BASE_DIR / ".tmp"
PIPELINE_DIR = TMP_DIR / "pipeline"

def get_session_dir(session_id: str) -> Path:
    """Helper to get and create session tmp directory."""
    s_dir = PIPELINE_DIR / session_id
    s_dir.mkdir(parents=True, exist_ok=True)
    return s_dir

def run_pipeline(prompt: str, use_cache: bool = True, session_id: str = None, use_vision: bool = True, use_vision_v2: bool = False) -> dict:
    """
    Coordinates and runs the complete ANDIP Multi-Agent Pipeline.
    Design DNA -> Brand -> Art Direction -> UX -> Motion -> Frontend -> Critic.
    
    use_vision_v2: If True, uses the 2-stage hybrid pipeline (faster, cheaper).
    """
    # 1. Initialize Session
    if not session_id:
        session_id = f"sess_{uuid.uuid4().hex[:12]}"
    
    session_dir = get_session_dir(session_id)
    print(f"\n==================================================")
    print(f"[START] INITIALIZING ANDIP PIPELINE RUN")
    print(f"Prompt: '{prompt[:60]}...'")
    print(f"Session ID: {session_id}")
    print(f"Session Dir: {session_dir}")
    print(f"==================================================\n")
    
    # 2. Check Cache
    prompt_hash = hashlib.md5(prompt.encode("utf-8")).hexdigest()
    cache_prefix = "blueprint_v2_" if use_vision_v2 else "blueprint_"
    cache_file = TMP_DIR / "cache" / f"{cache_prefix}{prompt_hash}.json"
    
    if use_cache and cache_file.exists():
        print(f"[CACHE HIT] Returning full cached Experience Blueprint for this prompt.")
        cached_data = json.loads(cache_file.read_text(encoding="utf-8"))
        # Save a copy to the session directory as well for record-keeping
        session_blueprint = session_dir / "experience_blueprint.json"
        session_blueprint.write_text(json.dumps(cached_data, indent=2, ensure_ascii=False), encoding="utf-8")
        return cached_data

    if use_vision_v2:
        print("[ORCHESTRATOR] Routing execution through Vision-First Pipeline V2 (2-Stage Hybrid)...")
        from execution.vision_pipeline_v2 import run_vision_pipeline_v2
        return run_vision_pipeline_v2(prompt, session_id=session_id)

    if use_vision:
        print("[ORCHESTRATOR] Routing execution through the Vision-First Pipeline (5-Stage)...")
        from execution.vision_pipeline import run_vision_pipeline
        return run_vision_pipeline(prompt, session_id=session_id)


    # Setup core session log dictionary
    session_log = {
        "metadata": {
            "session_id": session_id,
            "prompt": prompt,
            "revision_loops": 0,
            "warnings": [],
            "corrections": []
        },
        "steps": {}
    }

    # --- STEP 1: Discovery (Design DNA & Ontology Resolution) ---
    print(f"[STEP 1/7] Discovery & DNA Extraction...")
    # Extract simple DNA (caching handled inside prompt_analyzer)
    raw_dna = analyze_prompt(prompt, use_cache=use_cache)
    raw_dna["prompt_hint"] = prompt
    # Enrich and validate via Ontology Engine
    enriched_tokens = resolve_design_dna(raw_dna)
    
    # Track ontology warnings and corrections in session metadata
    session_log["metadata"]["warnings"].extend(enriched_tokens["metadata"]["applied_warnings"])
    session_log["metadata"]["corrections"].extend(enriched_tokens["metadata"]["applied_corrections"])
    
    # Save Step 1 Result
    session_log["steps"]["step_1_discovery"] = enriched_tokens
    (session_dir / "step_1_discovery.json").write_text(
        json.dumps(enriched_tokens, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    critic_feedback = ""
    loop_count = 0
    max_loops = 3
    
    while loop_count < max_loops:
        session_log["metadata"]["revision_loops"] = loop_count
        if loop_count > 0:
            print(f"\n[REVISION] ENTERING REVISION LOOP {loop_count}/{max_loops-1} (Critic Feedback injected)...")

        # --- STEP 1.5: Narrative Story Architecture (Enforced by Story Grammar) ---
        print(f"[STEP 1.5/7] Narrative Story Architecture...")
        story_scenes = execute_story_architect(enriched_tokens, critic_feedback=critic_feedback, model="anthropic/claude-3.5-sonnet")
        session_log["steps"]["step_1_5_story_scenes"] = story_scenes
        (session_dir / "step_1_5_story_scenes.json").write_text(
            json.dumps(story_scenes, indent=2, ensure_ascii=False), encoding="utf-8"
        )

        # --- STEP 2: Brand Strategy ---
        print(f"[STEP 2/7] Brand Strategy...")
        brand_identity = execute_brand_strategist(enriched_tokens, critic_feedback=critic_feedback, model="anthropic/claude-3.5-sonnet")
        session_log["steps"]["step_2_brand_strategy"] = brand_identity
        (session_dir / "step_2_brand_strategy.json").write_text(
            json.dumps(brand_identity, indent=2, ensure_ascii=False), encoding="utf-8"
        )
        
        # --- STEP 3: Art Direction ---
        print(f"[STEP 3/7] Art Direction...")
        visual_language = execute_art_director(enriched_tokens, brand_identity, critic_feedback=critic_feedback, model="anthropic/claude-3.5-sonnet")
        session_log["steps"]["step_3_art_direction"] = visual_language
        (session_dir / "step_3_art_direction.json").write_text(
            json.dumps(visual_language, indent=2, ensure_ascii=False), encoding="utf-8"
        )

        # --- STEP 4: UX Architecture (Enriched by Story Scenes) ---
        print(f"[STEP 4/7] UX Architecture...")
        # Incorporate story scenes into layout definition
        enriched_tokens_with_story = enriched_tokens.copy()
        enriched_tokens_with_story["story_scenes"] = story_scenes
        experience_flow = execute_ux_architect(enriched_tokens_with_story, brand_identity, visual_language, critic_feedback=critic_feedback, model="anthropic/claude-3.5-sonnet")
        session_log["steps"]["step_4_ux_architecture"] = experience_flow
        (session_dir / "step_4_ux_architecture.json").write_text(
            json.dumps(experience_flow, indent=2, ensure_ascii=False), encoding="utf-8"
        )

        # --- STEP 4.25: Scene Composition Layout Mapping ---
        print(f"[STEP 4.25/7] Scene Composition Layout Mapping...")
        scene_composition = execute_scene_composer(enriched_tokens, story_scenes, critic_feedback=critic_feedback, model="anthropic/claude-3.5-sonnet")
        session_log["steps"]["step_4_25_scene_composition"] = scene_composition
        (session_dir / "step_4_25_scene_composition.json").write_text(
            json.dumps(scene_composition, indent=2, ensure_ascii=False), encoding="utf-8"
        )

        # --- STEP 4.5: Spatial Experience & WebGL Director ---
        print(f"[STEP 4.5/7] Spatial Experience & WebGL Director...")
        webgl_choreography = execute_experience_director(enriched_tokens, story_scenes, critic_feedback=critic_feedback, model="anthropic/claude-3.5-sonnet")
        session_log["steps"]["step_4_5_webgl_choreography"] = webgl_choreography
        (session_dir / "step_4_5_webgl_choreography.json").write_text(
            json.dumps(webgl_choreography, indent=2, ensure_ascii=False), encoding="utf-8"
        )

        # --- STEP 5: Motion Direction ---
        print(f"[STEP 5/7] Motion Direction...")
        # Motion graph incorporates experience flow, WebGL choreography, and visual tokens
        motion_graph = execute_motion_director(enriched_tokens, visual_language, experience_flow, model="anthropic/claude-3.5-sonnet")
        motion_graph["webgl_choreography"] = webgl_choreography
        session_log["steps"]["step_5_motion_direction"] = motion_graph
        (session_dir / "step_5_motion_direction.json").write_text(
            json.dumps(motion_graph, indent=2, ensure_ascii=False), encoding="utf-8"
        )

        # --- STEP 6: Frontend Architecture (Component Mapping) ---
        print(f"[STEP 6/7] Component Mapping & Blueprint Generation...")
        # Component mapping runs on Haiku/Flash for fast, lightweight template binding
        component_plan = execute_component_mapper(enriched_tokens, visual_language, experience_flow, motion_graph, model="anthropic/claude-3-haiku")
        session_log["steps"]["step_6_frontend_arch"] = component_plan
        (session_dir / "step_6_frontend_arch.json").write_text(
            json.dumps(component_plan, indent=2, ensure_ascii=False), encoding="utf-8"
        )

        # --- STEP 7: Critic Audit ---
        print(f"[STEP 7/7] Design Critique & Quality Gate...")
        # Pack intermediate results up to here to send to critic
        current_session_data = {
            "dna": enriched_tokens,
            "brand_identity": brand_identity,
            "story_scenes": story_scenes,
            "visual_language": visual_language,
            "experience_flow": experience_flow,
            "scene_composition": scene_composition,
            "webgl_choreography": webgl_choreography,
            "motion_graph": motion_graph,
            "component_plan": component_plan
        }
        critic_report = execute_critic(current_session_data, model="anthropic/claude-3.5-sonnet")
        session_log["steps"]["step_7_critic"] = critic_report
        (session_dir / "step_7_critic.json").write_text(
            json.dumps(critic_report, indent=2, ensure_ascii=False), encoding="utf-8"
        )

        print(f"[CRITIC REPORT] Score = {critic_report.get('overall_score', 0)}/100 | Passes = {critic_report.get('passes_rules', False)}")
        
        # Check if audit is successful or loop limit is reached
        if critic_report.get("passes_rules", False) and critic_report.get("overall_score", 0) >= 80:
            print(f"[PASS] CRITIC PASSED! final blueprint locked.")
            break
        else:
            failures = critic_report.get("failures", [])
            recommendations = critic_report.get("recommendations", [])
            critic_feedback = f"Failures: {', '.join(failures)}\nRecommendations: {', '.join(recommendations)}"
            loop_count += 1
            
            if loop_count >= max_loops:
                print(f"[WARNING] CRITIC LIMIT REACHED. Forcing lock on the latest blueprint.")
                session_log["metadata"]["warnings"].append({
                    "rule_id": "CRITIC_MAX_REVISIONS",
                    "message": "Critic revision loops reached the maximum allowance (3). Proceeding with current values."
                })
                break
    
    # 3. Assemble and Save Final Experience Blueprint JSON
    experience_blueprint = {
        "metadata": session_log["metadata"],
        "design_dna": enriched_tokens,
        "story_scenes": session_log["steps"]["step_1_5_story_scenes"],
        "brand_identity": session_log["steps"]["step_2_brand_strategy"],
        "visual_language": session_log["steps"]["step_3_art_direction"],
        "experience_flow": session_log["steps"]["step_4_ux_architecture"],
        "scene_composition": session_log["steps"]["step_4_25_scene_composition"],
        "webgl_choreography": session_log["steps"]["step_4_5_webgl_choreography"],
        "motion_graph": session_log["steps"]["step_5_motion_direction"],
        "component_plan": session_log["steps"]["step_6_frontend_arch"],
        "critique_report": session_log["steps"]["step_7_critic"]
    }
    
    # Save to session directory
    (session_dir / "experience_blueprint.json").write_text(
        json.dumps(experience_blueprint, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    
    # Save to prompt cache directory
    (TMP_DIR / "cache").mkdir(parents=True, exist_ok=True)
    cache_file.write_text(
        json.dumps(experience_blueprint, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    
    print(f"\n[SUCCESS] PIPELINE COMPLETED SUCCESSFULLY!")
    print(f"Blueprint saved at: {session_dir / 'experience_blueprint.json'}")
    print(f"==================================================\n")
    
    return experience_blueprint

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="ANDIP Multi-Agent Experience Pipeline Orchestrator")
    parser.add_argument("prompt", type=str, nargs="?", help="Design inspiration prompt")
    parser.add_argument("--no-cache", action="store_true", help="Disable cache for prompt analysis")
    parser.add_argument("--no-vision", action="store_true", help="Disable visual vision-first pipeline (use text-only)")
    args = parser.parse_args()
    
    if args.prompt:
        blueprint = run_pipeline(args.prompt, use_cache=not args.no_cache, use_vision=not args.no_vision)
    else:
        # Dry run with sample prompt
        sample_prompt = "Sitem hem inanılmaz derecede lüks, premium ve minimalist hissettirmeli hem de sokak kültürünün o asi, kaotik, grafitili ve hırçın enerjisini taşımalı."
        print(f"Dry running pipeline with default prompt: '{sample_prompt}'")
        run_pipeline(sample_prompt, use_cache=False, use_vision=not args.no_vision)

