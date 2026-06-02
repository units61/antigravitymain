import sys
import json
from pathlib import Path

# Add project root and execution directory to system path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from execution.pipeline_runner import run_pipeline

TEST_PROMPTS = [
    # 1. Luxury Rebel (Turkish)
    "Sitem hem inanılmaz derecede lüks, premium ve minimalist hissettirmeli hem de sokak kültürünün o asi, kaotik, grafitili ve hırçın enerjisini taşımalı.",
    # 2. Melancholic Calm (Turkish)
    "Bana bir kış sabahı sislerin arasından doğan güneşin verdiği o huzurlu ama melankolik hissi veren bir arayüz tasarla.",
    # 3. Cyberpunk Brutalist (English)
    "A fast, dense, matrix-style cyber security dashboard.",
    # 4. Playful Educational (English)
    "A fun, bouncy learning app for kids with bright colors and physical bouncing cards.",
    # 5. Minimal Editorial (English)
    "An elegant, typography-heavy fashion magazine style editorial shop."
]

def assert_blueprint_structure(blueprint: dict):
    """Asserts that the final blueprint JSON is fully populated and valid."""
    assert "metadata" in blueprint, "Missing metadata in blueprint"
    assert "design_dna" in blueprint, "Missing design_dna in blueprint"
    assert "brand_identity" in blueprint, "Missing brand_identity in blueprint"
    assert "visual_language" in blueprint, "Missing visual_language in blueprint"
    assert "experience_flow" in blueprint, "Missing experience_flow in blueprint"
    assert "motion_graph" in blueprint, "Missing motion_graph in blueprint"
    assert "component_plan" in blueprint, "Missing component_plan in blueprint"
    assert "critique_report" in blueprint, "Missing critique_report in blueprint"
    
    # Assert specific fields
    assert blueprint["brand_identity"].get("brand_name"), "Missing brand_name in brand strategy"
    assert blueprint["visual_language"].get("color_tokens"), "Missing color_tokens in art direction"
    assert len(blueprint["experience_flow"].get("sections", [])) > 0, "No sections designed in UX"
    assert blueprint["critique_report"].get("overall_score") is not None, "Critic did not issue a score"
    print("[SUCCESS] Assertions passed! Blueprint structure is 100% valid.")

def test_single_prompt(index: int):
    """Runs integration test for a specific prompt index."""
    if index < 0 or index >= len(TEST_PROMPTS):
        print(f"Invalid prompt index: {index}")
        return
        
    prompt = TEST_PROMPTS[index]
    print(f"\n==================================================")
    print(f"[TEST] RUNNING PIPELINE INTEGRATION TEST (PROMPT {index + 1})")
    print(f"Prompt: '{prompt}'")
    print(f"==================================================")
    
    try:
        # Run pipeline (caching enabled to save tokens during development)
        blueprint = run_pipeline(prompt, use_cache=True, session_id=f"test_run_{index + 1}")
        
        # Verify and assert structure
        assert_blueprint_structure(blueprint)
        
        print(f"\n[PASS] TEST {index + 1} PASSED SUCCESSFULLY!")
        print(f"Critic overall score: {blueprint['critique_report'].get('overall_score')}")
        print(f"Revision loops completed: {blueprint['metadata'].get('revision_loops')}")
        print(f"Applied Corrections count: {len(blueprint['metadata'].get('corrections', []))}")
        print(f"Applied Warnings count: {len(blueprint['metadata'].get('warnings', []))}")
        
    except Exception as e:
        print(f"\n[FAIL] TEST {index + 1} FAILED WITH ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="ANDIP Multi-Agent Pipeline Integration Test Suite")
    parser.add_argument("--index", type=int, default=0, help="Test prompt index to run (0-4)")
    parser.add_argument("--all", action="store_true", help="Run all 5 integration tests")
    args = parser.parse_args()
    
    if args.all:
        print(f"Starting execution of all {len(TEST_PROMPTS)} integration tests...")
        for i in range(len(TEST_PROMPTS)):
            test_single_prompt(i)
    else:
        test_single_prompt(args.index)
