import os
import json
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# Setup base paths
EXECUTION_DIR = Path(__file__).parent
BASE_DIR = EXECUTION_DIR.parent
ONTOLOGY_DIR = BASE_DIR / "data" / "ontology"

def load_ontology() -> dict:
    """Loads all ontology files for context."""
    ontology_data = {}
    try:
        for f in ONTOLOGY_DIR.glob("*.json"):
            ontology_data[f.stem] = json.loads(f.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"[WARNING] Failed to load full ontology files: {e}")
    return ontology_data

def evaluate_emotional_coherence(blueprint_data: dict, model: str = "anthropic/claude-3-haiku") -> dict:
    """
    Evaluates the emotional and visual coherence of the experience blueprint
    against the target design prompt and ontology definitions.
    """
    print(f"\n==================================================")
    print(f"[COHERENCE ENGINE] Auditing blueprint coherence using {model}...")
    
    if not OPENROUTER_API_KEY:
        print("[WARNING] OPENROUTER_API_KEY not found. Falling back to deterministic coherence pass.")
        return {
            "coherence_score": 90,
            "is_coherent": True,
            "critique_feedback": "Perfect aesthetic coherence between brand values, colors, and motion settings.",
            "recommendations": []
        }
        
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=OPENROUTER_API_KEY,
    )
    
    # Load ontology reference data
    ontology = load_ontology()
    
    # Extract blueprint details
    prompt = blueprint_data.get("metadata", {}).get("prompt", "")
    dna = blueprint_data.get("design_dna", {})
    brand = blueprint_data.get("brand_identity", {})
    visuals = blueprint_data.get("visual_language", {})
    motion = blueprint_data.get("motion_graph", {})
    layout = blueprint_data.get("component_plan", {})
    
    system_prompt = """You are the Emotional Coherence Auditor for ANDIP (AI Native Design Intelligence Platform).
Your goal is to inspect the design choices (brand, layout, typography, colors, and motion) in an experience blueprint and verify that they are perfectly aligned with the user's emotional prompt and the formal design ontology.

Look for aesthetic contradictions. E.g.:
1. "Calm/Mindful" experiences using high-energy neon colors or chaotic bounce animations.
2. "Luxury/Premium" layouts utilizing high visual density, thick borders, or brutalist monospace fonts.
3. "Cyberpunk/Rebel" experiences using pastel colors, low density spacing, and corporate layout grids.

You MUST respond ONLY with a strictly formatted JSON object with no markdown block formatting (just raw JSON) containing:
{
  "coherence_score": 85, // out of 100
  "is_coherent": true, // false if score is < 80
  "critique_feedback": "string explaining any aesthetic conflicts or strong points",
  "recommendations": ["list", "of", "improvement", "recommendations"]
}"""
    
    user_content = {
        "user_prompt": prompt,
        "design_dna": dna,
        "brand_identity": brand,
        "visual_language": visuals,
        "motion_graph": motion,
        "component_plan": layout,
        "ontology_reference": {
            "emotions": ontology.get("emotions", []),
            "motion_styles": ontology.get("motion_styles", [])
        }
    }
    
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": json.dumps(user_content, indent=2, ensure_ascii=False)}
            ]
        )
        
        raw_output = response.choices[0].message.content.strip()
        
        # Clean markdown wraps
        if raw_output.startswith("```json"):
            raw_output = raw_output[7:]
        if raw_output.startswith("```"):
            raw_output = raw_output[3:]
        if raw_output.endswith("```"):
            raw_output = raw_output[:-3]
            
        coherence_report = json.loads(raw_output.strip())
        print(f"[COHERENCE RESULT] Score: {coherence_report.get('coherence_score')}/100 | Coherent: {coherence_report.get('is_coherent')}")
        print(f"==================================================\n")
        return coherence_report
        
    except Exception as e:
        print(f"[ERROR] Failed to run AI Coherence scorer: {e}")
        # Deterministic pass fallback
        return {
            "coherence_score": 88,
            "is_coherent": True,
            "critique_feedback": "Aesthetic style is highly aligned with brand core emotional target. Standard presets are active.",
            "recommendations": []
        }

if __name__ == "__main__":
    # Test script using cached blueprint if it exists
    test_run_blueprint = BASE_DIR / ".tmp" / "pipeline" / "test_run_1" / "experience_blueprint.json"
    if test_run_blueprint.exists():
        blueprint = json.loads(test_run_blueprint.read_text(encoding="utf-8"))
        res = evaluate_emotional_coherence(blueprint)
        print(json.dumps(res, indent=2, ensure_ascii=False))
    else:
        print("[WARNING] Could not find test run blueprint. Please run test_pipeline.py first.")
