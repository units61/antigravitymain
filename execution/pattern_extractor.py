import os
import json
import hashlib
from pathlib import Path

# Setup base paths
EXECUTION_DIR = Path(__file__).parent
BASE_DIR = EXECUTION_DIR.parent
PATTERNS_DIR = BASE_DIR / "data" / "patterns"

def extract_and_save_pattern(blueprint: dict) -> dict:
    """
    Analyzes an experience blueprint. If the score is >= 88/100,
    extracts the layout/motion sequence and appends it to the patterns registry.
    """
    print(f"\n==================================================")
    print(f"[LEARNING ENGINE] ANALYZING DESIGN FOR PATTERN EXTRACTION")
    
    metadata = blueprint.get("metadata", {})
    session_id = metadata.get("session_id", "sess_unknown")
    prompt = metadata.get("prompt", "")
    
    critique = blueprint.get("critique_report", {})
    score = critique.get("overall_score", 0)
    
    print(f"Session: {session_id} | Score: {score}/100")
    
    # 1. Check learning threshold
    THRESHOLD = 88
    if score < THRESHOLD:
        print(f"[LEARNING BYPASSED] Score ({score}) is below learning threshold ({THRESHOLD}).")
        print(f"==================================================\n")
        return {"learned": False, "reason": f"Score {score} < {THRESHOLD}"}
        
    print(f"[LEARNING TRIGGERED] High quality design detected! Extracting pattern...")
    
    dna = blueprint.get("design_dna", {})
    brand = blueprint.get("brand_identity", {})
    visuals = blueprint.get("visual_language", {})
    motion = blueprint.get("motion_graph", {})
    components = blueprint.get("component_plan", {}).get("mapped_components", [])
    
    if not components:
        print("[LEARNING WARNING] No components found to map.")
        print(f"==================================================\n")
        return {"learned": False, "reason": "No components in blueprint"}
        
    # 2. Build the pattern details
    # Generate clean ID based on prompt hash to prevent duplicate insertions
    prompt_hash = hashlib.md5(prompt.encode("utf-8")).hexdigest()[:8]
    pattern_id = f"learned-flow-{prompt_hash}"
    
    category = "hero"
    best_for = [dna.get("core_emotion", "editorial")]
    if dna.get("brand_archetype"):
        best_for.append(dna.get("brand_archetype"))
        
    recommended = [comp.get("component_id") for comp in components]
    
    new_pattern = {
        "id": pattern_id,
        "name": f"Self-Learned {dna.get('brand_archetype', 'Creative').capitalize()} Flow",
        "category": category,
        "best_for": best_for,
        "emotion_scores": {
            dna.get("core_emotion", "editorial"): 9,
            "learned_success": 10
        },
        "motion_energy": motion.get("motion_budget", {}).get("total_budget", 5),
        "performance_cost": 4,
        "layout_type": dna.get("spatial_mode", "airy"),
        "requires_3d": False,
        "scroll_behavior": dna.get("motion_style", "cinematic"),
        "recommended_components": recommended,
        "conversion_strength": 9,
        "mobile_adaptation": "standard-padding",
        "learned_from_session": session_id,
        "original_prompt": prompt
    }
    
    # 3. Read and update patterns file
    patterns_file = PATTERNS_DIR / "hero_patterns.json"
    patterns_list = []
    
    if patterns_file.exists():
        try:
            patterns_list = json.loads(patterns_file.read_text(encoding="utf-8"))
        except Exception as e:
            print(f"[LEARNING ERROR] Could not parse patterns database: {e}")
            
    # Check if this exact pattern already exists
    exists = False
    for p in patterns_list:
        if p.get("id") == pattern_id:
            exists = True
            print(f"[LEARNING BYPASSED] Pattern with ID '{pattern_id}' already exists in registry.")
            break
            
    if not exists:
        patterns_list.append(new_pattern)
        patterns_file.parent.mkdir(parents=True, exist_ok=True)
        patterns_file.write_text(json.dumps(patterns_list, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"[LEARNING SUCCESS] Successfully recorded new learned pattern '{new_pattern['name']}' to {patterns_file}!")
        
    print(f"==================================================\n")
    return {"learned": not exists, "pattern_id": pattern_id, "pattern": new_pattern}

if __name__ == "__main__":
    # Test learning loop using cached blueprint if available
    test_run_blueprint = BASE_DIR / ".tmp" / "pipeline" / "test_run_1" / "experience_blueprint.json"
    if test_run_blueprint.exists():
        blueprint = json.loads(test_run_blueprint.read_text(encoding="utf-8"))
        # Force high critic score for testing purposes
        blueprint["critique_report"]["overall_score"] = 92
        extract_and_save_pattern(blueprint)
    else:
        print("[WARNING] Could not find test run blueprint. Run test_pipeline.py first.")
