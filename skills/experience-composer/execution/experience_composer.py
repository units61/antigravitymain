import os
import json
import sys
from pathlib import Path

# Add project root and execution directory to system path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.append(str(project_root))

from execution.pipeline_runner import run_pipeline

def get_directive() -> str:
    directive_path = Path(__file__).parent.parent / "SKILL.md"
    return directive_path.read_text(encoding="utf-8")

def execute_experience_composer(input_data: dict) -> dict:
    """
    Main execution logic for experience-composer.
    Calls our complete multi-agent design pipeline.
    """
    prompt = input_data.get("prompt", "")
    if not prompt:
        raise ValueError("Missing required key 'prompt' in experience-composer input.")
    
    use_cache = input_data.get("use_cache", True)
    session_id = input_data.get("session_id", None)
    
    blueprint = run_pipeline(prompt, use_cache=use_cache, session_id=session_id)
    return {
        "status": "success",
        "data": blueprint
    }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        print(json.dumps(execute_experience_composer(json.loads(sys.argv[1])), indent=2, ensure_ascii=False))
    else:
        print("Usage: python experience_composer.py '<json_input>'")

