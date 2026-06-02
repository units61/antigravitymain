import os
from pathlib import Path

skills = [
    "ontology-manager",
    "pattern-matcher",
    "experience-composer",
    "component-selector",
    "motion-director",
    "design-critic"
]

base_dir = Path("skills")

for skill in skills:
    skill_dir = base_dir / skill
    exec_dir = skill_dir / "execution"
    exec_dir.mkdir(parents=True, exist_ok=True)
    
    # 1. Create SKILL.md
    skill_md = skill_dir / "SKILL.md"
    skill_md.write_text(f"""# Directive: {skill.replace('-', ' ').title()}

## Objective
Define the goal and rules for the {skill} skill.

## System Instructions
You are an expert AI agent responsible for {skill.replace('-', ' ')}. 
Follow the rules strictly and output valid JSON.

## Output Schema
```json
{{
  "status": "success",
  "data": {{}}
}}
```
""", encoding="utf-8")
    
    # 2. Create python execution script
    script_name = skill.replace('-', '_') + ".py"
    py_script = exec_dir / script_name
    py_script.write_text(f"""import os
import json
from pathlib import Path

def get_directive() -> str:
    directive_path = Path(__file__).parent.parent / "SKILL.md"
    return directive_path.read_text(encoding="utf-8")

def execute_{script_name.replace('.py', '')}(input_data: dict) -> dict:
    \"\"\"
    Main execution logic for {skill}.
    \"\"\"
    # TODO: Implement OpenAI/OpenRouter API call with get_directive()
    print(f"Executing {skill} with input: {{input_data}}")
    return {{"status": "success", "data": {{}}}}

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        print(json.dumps(execute_{script_name.replace('.py', '')}(json.loads(sys.argv[1])), indent=2))
    else:
        print("Usage: python {script_name} '<json_input>'")
""", encoding="utf-8")

    # 3. Create test script
    test_script = exec_dir / f"test_{script_name}"
    test_script.write_text(f"""import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))
from {script_name.replace('.py', '')} import execute_{script_name.replace('.py', '')}

def run_tests():
    print("=== RUNNING SKILL TESTS: {skill.upper()} ===")
    test_input = {{"example": "data"}}
    try:
        result = execute_{script_name.replace('.py', '')}(test_input)
        print("Result:", result)
    except Exception as e:
        print(f"Error: {{e}}")

if __name__ == "__main__":
    run_tests()
""", encoding="utf-8")

print("All skill scaffolds created successfully.")
