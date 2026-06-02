import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))
from component_selector import execute_component_selector

def run_tests():
    print("=== RUNNING SKILL TESTS: COMPONENT-SELECTOR ===")
    test_input = {"example": "data"}
    try:
        result = execute_component_selector(test_input)
        print("Result:", result)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    run_tests()
