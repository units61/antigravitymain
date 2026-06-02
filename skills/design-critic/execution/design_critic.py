import os
import json
import sys
from pathlib import Path

# Add project root and execution directory to system path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.append(str(project_root))

from execution.critic import execute_critic

def get_directive() -> str:
    directive_path = Path(__file__).parent.parent / "SKILL.md"
    return directive_path.read_text(encoding="utf-8")

def execute_design_critic(input_data: dict) -> dict:
    """
    Main execution logic for design-critic.
    """
    # Simply invoke our central critic execution
    model = input_data.get("model", "anthropic/claude-3-haiku")
    result = execute_critic(input_data, model=model)
    return {
        "status": "success",
        "data": result
    }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        print(json.dumps(execute_design_critic(json.loads(sys.argv[1])), indent=2, ensure_ascii=False))
    else:
        print("Usage: python design_critic.py '<json_input>'")

