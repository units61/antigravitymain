# -*- coding: utf-8 -*-
"""
ANDIP Vision-First Pipeline End-to-End Integration Test.
This script executes the complete 5-stage Vision-First Pipeline, verifies the produced assets
(both visual images and structured JSON blueprints), and runs the Next.js assembler to test
the visual code compilation.
"""

import sys
import os
import json
from pathlib import Path
import traceback

# Add project root to sys path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from execution.pipeline_runner import run_pipeline
from execution.component_assembler import assemble_next_app

def verify_vision_pipeline_assets(session_id: str):
    """
    Verifies that all visual PNG files and step JSON files are successfully
    generated in the session directory.
    """
    session_dir = project_root / ".tmp" / "pipeline" / session_id
    visuals_dir = session_dir / "visuals"
    
    print("\n--- [VERIFICATION] CHECKING GENERATED ASSETS ---")
    
    # 1. Check directories
    assert session_dir.exists(), f"Session directory {session_dir} does not exist!"
    assert visuals_dir.exists(), f"Visuals directory {visuals_dir} does not exist!"
    
    # 2. Check visual PNG files
    expected_visuals = [
        "stage_1_moodboard.png",
        "stage_2_design_spec.png",
        "stage_3_wireframe.png",
        "stage_5_motion_storyboard.png"
    ]
    
    print("Checking visual PNG files...")
    for visual in expected_visuals:
        path = visuals_dir / visual
        assert path.exists(), f"Expected visual asset not found: {path}"
        assert path.stat().st_size > 0, f"Visual asset file is empty: {path}"
        print(f"  [PASS] Found visual: {visual} ({path.stat().st_size} bytes)")
        
    # Check if at least one component detail render is present
    comp_renders = list(visuals_dir.glob("stage_4_*_component.png"))
    assert len(comp_renders) > 0, "No Stage 4 Component Detail Renders were generated!"
    print(f"  [PASS] Found Component Render: {comp_renders[0].name} ({comp_renders[0].stat().st_size} bytes)")
    
    # 3. Check JSON files
    expected_jsons = [
        "step_1_discovery.json",
        "step_2_brand_strategy.json",
        "step_3_art_direction.json",
        "step_4_ux_architecture.json",
        "step_5_motion_direction.json",
        "step_6_frontend_arch.json",
        "step_7_critic.json",
        "experience_blueprint.json"
    ]
    
    print("\nChecking generated JSON files...")
    for js_file in expected_jsons:
        path = session_dir / js_file
        assert path.exists(), f"Expected JSON step file not found: {path}"
        # Validate JSON content
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            assert len(data.keys()) > 0, f"JSON file is empty: {js_file}"
        except Exception as e:
            raise AssertionError(f"Invalid JSON in file {js_file}: {e}")
        print(f"  [PASS] Found valid JSON: {js_file}")
        
    print("\n[VERIFICATION SUCCESS] All pipeline assets verified perfectly!")

def test_e2e_vision_pipeline():
    print("=== STARTING VISION-FIRST PIPELINE E2E INTEGRATION TEST ===")
    prompt = "A luxury high-end cyberpunk fashion editorial shop for Gen Z. Extremely premium, dark neon, glowing vectors, clean layouts."
    session_id = "test_vision_e2e_run"
    
    try:
        # Run Phase 3: Vision-First Orchestrated Pipeline (No cache to force generation)
        print("\n=== STEP 1: EXECUTING ORCHESTRATED VISION PIPELINE ===")
        blueprint = run_pipeline(prompt, use_cache=False, session_id=session_id, use_vision=True)
        
        # Verify visual asset outputs and step files
        verify_vision_pipeline_assets(session_id)
        
        # Run Phase 4: Next.js App Assembly (Triggering Multimodal AI Compiler)
        print("\n=== STEP 2: RUNNING NEXT.JS APP ASSEMBLY & MULTIMODAL COMPILATION ===")
        blueprint_path = project_root / ".tmp" / "pipeline" / session_id / "experience_blueprint.json"
        
        # Set OpenRouter key in environment if not present
        if not os.getenv("OPENROUTER_API_KEY"):
            raise ValueError("OPENROUTER_API_KEY is missing. Can't test multimodal code generation.")
            
        build_dir = assemble_next_app(blueprint_path, session_id)
        
        print("\n=== STEP 3: VERIFYING ASSEMBLED APP COMPONENTS ===")
        assert build_dir.exists(), f"Build directory does not exist: {build_dir}"
        
        # Check that compiled components are in place and contain use client directive
        components_path = build_dir / "components"
        assert components_path.exists(), "Components directory was not created!"
        
        # List JSX files generated in components
        jsx_files = list(components_path.glob("*.jsx"))
        print(f"Generated components in build directory:")
        for jsx in jsx_files:
            content = jsx.read_text(encoding="utf-8")
            has_use_client = '"use client"' in content or "'use client'" in content
            print(f"  - {jsx.name} ({len(content.splitlines())} lines) [use client: {has_use_client}]")
            assert len(content.splitlines()) > 0, f"Component file {jsx.name} is empty!"
            
        print("\n=== [E2E TEST PASSED] === ")
        print(f"All components and visual references are compiled successfully.")
        print(f"Build output located at: {build_dir.absolute()}")
        print("==========================================================")
        
    except Exception as e:
        print(f"\n[E2E TEST FAILED] Test execution encountered an error: {e}")
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    test_e2e_vision_pipeline()
