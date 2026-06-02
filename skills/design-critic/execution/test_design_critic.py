import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))
from design_critic import execute_design_critic

def run_tests():
    print("=== RUNNING SKILL TESTS: DESIGN-CRITIC ===")
    test_input = {"example": "data"}
    try:
        result = execute_design_critic(test_input)
        print("Result:", result)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    run_tests()
