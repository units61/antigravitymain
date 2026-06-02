import os
import json
import sys
from pathlib import Path

# Add project root and execution directory to system path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.append(str(project_root))

from execution.motion_director import execute_motion_director as run_motion_director

def get_directive() -> str:
    directive_path = Path(__file__).parent.parent / "SKILL.md"
    return directive_path.read_text(encoding="utf-8")

def execute_motion_director(input_data: dict) -> dict:
    """
    Main execution logic for motion-director.
    """
    # Extract sub-fields from dynamic input data
    enriched_tokens = input_data.get("dna", {})
    visual_language = input_data.get("visual_language", {})
    experience_flow = input_data.get("experience_flow", {})
    model = input_data.get("model", "anthropic/claude-3-haiku")
    
    result = run_motion_director(enriched_tokens, visual_language, experience_flow, model=model)
    return {
        "status": "success",
        "data": result
    }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        print(json.dumps(execute_motion_director(json.loads(sys.argv[1])), indent=2, ensure_ascii=False))
    else:
        print("Usage: python motion_director.py '<json_input>'")

