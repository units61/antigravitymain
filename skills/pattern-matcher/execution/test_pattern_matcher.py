import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))
from pattern_matcher import execute_pattern_matcher

def run_tests():
    print("=== RUNNING SKILL TESTS: PATTERN-MATCHER ===")
    test_input = {"example": "data"}
    try:
        result = execute_pattern_matcher(test_input)
        print("Result:", result)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    run_tests()
