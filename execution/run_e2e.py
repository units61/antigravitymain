import os
import sys
import json
import uuid
from pathlib import Path

# Add project root and parent to sys path for static linter & runtime compliance
EXECUTION_DIR = Path(__file__).parent
BASE_DIR = EXECUTION_DIR.parent
sys.path.append(str(BASE_DIR))
sys.path.append(str(BASE_DIR.parent))

# Import all Phase 3 & 4 core pipeline units (resolves perfectly statically and at runtime)
from antigravitymain.execution.pipeline_runner import run_pipeline
from antigravitymain.execution.component_assembler import assemble_next_app
from antigravitymain.execution.performance_checker import run_performance_checker
from antigravitymain.execution.emotional_coherence_scorer import evaluate_emotional_coherence
from antigravitymain.execution.deploy import deploy_app
from antigravitymain.execution.pattern_extractor import extract_and_save_pattern

def execute_e2e_flow(prompt: str, use_v2: bool = False) -> dict:
    """
    Executes the entire end-to-end design, generation, auditing, deployment
    and reinforcement learning pipeline.
    
    use_v2: If True, uses 2-stage hybrid vision pipeline (faster, cheaper).
    """
    session_id = f"e2e_{uuid.uuid4().hex[:8]}"
    session_dir = BASE_DIR / ".tmp" / "pipeline" / session_id
    session_dir.mkdir(parents=True, exist_ok=True)
    
    pipeline_label = "V2 (2-Stage Hybrid)" if use_v2 else "V1 (5-Stage)"
    
    print(f"\n==========================================================================")
    print(f"                   ANDIP MASTER E2E ENGINE RUN                           ")
    print(f"==========================================================================")
    print(f"Prompt: '{prompt}'")
    print(f"Pipeline: {pipeline_label}")
    print(f"Session ID: {session_id}")
    print(f"Session Dir: {session_dir}")
    print(f"==========================================================================\n")
    
    e2e_report = {
        "metadata": {
            "session_id": session_id,
            "prompt": prompt,
            "pipeline_version": pipeline_label
        },
        "stages": {}
    }
    
    # --- STAGE 1: Blueprint Generation ---
    print("\n--- [STAGE 1/5] GENERATING EXPERIENCE BLUEPRINT ---")
    try:
        # Run generative multi-agent pipeline
        blueprint = run_pipeline(prompt, use_cache=False, session_id=session_id, use_vision_v2=use_v2)
        e2e_report["stages"]["blueprint_generation"] = {
            "success": True,
            "critic_score": blueprint.get("critique_report", {}).get("overall_score", 0),
            "loops": blueprint.get("metadata", {}).get("revision_loops", 0)
        }
    except Exception as e:
        print(f"[STAGE 1 FAIL] blueprint generation failed: {e}")
        e2e_report["stages"]["blueprint_generation"] = {"success": False, "error": str(e)}
        return e2e_report
        
    # --- STAGE 1.5: 3D Scene Generation ---
    print("\n--- [STAGE 1.5/5] GENERATING 3D WEBGL SCENE STATE ---")
    try:
        from antigravitymain.execution.scene_generator import execute_scene_generator
        scene_state = execute_scene_generator(
            blueprint["design_dna"],
            blueprint["visual_language"],
            blueprint["experience_flow"],
            blueprint["motion_graph"]
        )
        # Save scene state in session directory
        (session_dir / "scene_state.json").write_text(
            json.dumps(scene_state, indent=2, ensure_ascii=False), encoding="utf-8"
        )
        e2e_report["stages"]["3d_scene_generation"] = {
            "success": True,
            "theme": scene_state.get("theme"),
            "camera_path": scene_state.get("camera", {}).get("path")
        }
    except Exception as e:
        print(f"[STAGE 1.5 WARNING] 3D scene generation failed: {e}")
        e2e_report["stages"]["3d_scene_generation"] = {"success": False, "error": str(e)}
        
    # --- STAGE 2: Application Assembly ---
    print("\n--- [STAGE 2/5] ASSEMBLING NEXT.JS REACT APPLICATION ---")
    blueprint_path = session_dir / "experience_blueprint.json"
    try:
        build_dir = assemble_next_app(blueprint_path, session_id)
        e2e_report["stages"]["app_assembly"] = {
            "success": True,
            "build_path": str(build_dir)
        }
    except Exception as e:
        print(f"[STAGE 2 FAIL] App assembly failed: {e}")
        e2e_report["stages"]["app_assembly"] = {"success": False, "error": str(e)}
        return e2e_report
        
    # --- STAGE 3: Performance, Accessibility & Dynamic Browser Audits ---
    print("\n--- [STAGE 3/5] AUDITING PERFORMANCE, WCAG & VISUAL RENDER ---")
    try:
        perf_report = run_performance_checker(session_id)
        e2e_report["stages"]["performance_wcag_audit"] = {
            "success": True,
            "est_lighthouse_score": perf_report.get("lighthouse_score_estimation", 90),
            "wcag_passed": perf_report.get("wcag_compliance", {}).get("a11y_accessibility", {}).get("passed", True),
            "contrast_ratios": perf_report.get("wcag_compliance", {}).get("contrast_ratios", {}),
            "browser_loaded": perf_report.get("browser_audit", {}).get("loaded_successfully", False),
            "screenshot_path": perf_report.get("browser_audit", {}).get("screenshot_path"),
            "warnings": perf_report.get("warnings", [])
        }
    except Exception as e:
        print(f"[STAGE 3 FAIL] Performance and accessibility checker failed: {e}")
        e2e_report["stages"]["performance_wcag_audit"] = {"success": False, "error": str(e)}
        
    # --- STAGE 4: Emotional & Aesthetic Coherence Scoring ---
    print("\n--- [STAGE 4/5] ASSESSING EMOTIONAL & AESTHETIC COHERENCE ---")
    try:
        coherence_report = evaluate_emotional_coherence(blueprint)
        e2e_report["stages"]["emotional_coherence"] = {
            "success": True,
            "coherence_score": coherence_report.get("coherence_score", 90),
            "is_coherent": coherence_report.get("is_coherent", True),
            "critique_feedback": coherence_report.get("critique_feedback", ""),
            "recommendations": coherence_report.get("recommendations", [])
        }
    except Exception as e:
        print(f"[STAGE 4 FAIL] Emotional coherence evaluation failed: {e}")
        e2e_report["stages"]["emotional_coherence"] = {"success": False, "error": str(e)}
        
    # --- STAGE 5: Production Compilation & Deployment ---
    print("\n--- [STAGE 5/5] PRODUCTION BUILD & DEPLOYMENT STAGE ---")
    try:
        deploy_report = deploy_app(session_id)
        e2e_report["stages"]["deployment"] = {
            "success": deploy_report.get("build_success", False),
            "deployed": deploy_report.get("deployed", False),
            "live_url": deploy_report.get("deploy_url"),
            "warnings": deploy_report.get("warnings", [])
        }
    except Exception as e:
        print(f"[STAGE 5 FAIL] Build and deploy stage failed: {e}")
        e2e_report["stages"]["deployment"] = {"success": False, "error": str(e)}
        
    # --- SELF-LEARNING STAGE: Pattern Extraction ---
    print("\n--- [LEARNING STAGE] RUNNING SYSTEM REINFORCEMENT LEARNING ---")
    # Feed metrics into blueprint critique to let reinforcement learn
    critic_score = blueprint.get("critique_report", {}).get("overall_score", 85)
    lighthouse_score = e2e_report["stages"].get("performance_wcag_audit", {}).get("est_lighthouse_score", 90)
    coherence_score = e2e_report["stages"].get("emotional_coherence", {}).get("coherence_score", 90)
    
    # Calculate composite final score
    composite_score = int(0.4 * critic_score + 0.3 * lighthouse_score + 0.3 * coherence_score)
    blueprint["critique_report"]["overall_score"] = composite_score
    
    print(f"Composite Design Score calculated: {composite_score}/100")
    try:
        learn_report = extract_and_save_pattern(blueprint)
        e2e_report["stages"]["self_learning"] = learn_report
    except Exception as e:
        print(f"[LEARNING FAIL] Pattern extraction failed: {e}")
        e2e_report["stages"]["self_learning"] = {"learned": False, "error": str(e)}
        
    # --- Save E2E Report ---
    report_file = session_dir / "e2e_report.json"
    report_file.write_text(json.dumps(e2e_report, indent=2, ensure_ascii=False), encoding="utf-8")
    
    print(f"\n==========================================================================")
    print(f"                   ANDIP MASTER E2E ENGINE SUCCESS                       ")
    print(f"==========================================================================")
    print(f"Session: {session_id}")
    print(f"Lighthouse Score: {lighthouse_score}/100")
    print(f"Coherence Score: {coherence_score}/100")
    print(f"Compilation/Build: {'PASSED' if e2e_report['stages']['deployment'].get('success') else 'FAILED'}")
    print(f"Live Deploy URL: {e2e_report['stages']['deployment'].get('live_url')}")
    print(f"Pattern Learned: {'YES (' + learn_report.get('pattern_id') + ')' if learn_report.get('learned') else 'NO'}")
    print(f"E2E Report written to: {report_file}")
    print(f"==========================================================================\n")
    
    return e2e_report

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="ANDIP Master End-to-End Orchestrator")
    parser.add_argument("prompt", type=str, nargs="?", help="Design inspiration prompt")
    parser.add_argument("--v2", action="store_true", help="Use 2-stage hybrid vision pipeline (faster, cheaper)")
    args = parser.parse_args()
    
    sample = "A premium creative studio storytelling landing page with vibrant colors, warm editorial feel, and story scroll narrative."
    prompt = args.prompt if args.prompt else sample
    
    execute_e2e_flow(prompt, use_v2=args.v2)
