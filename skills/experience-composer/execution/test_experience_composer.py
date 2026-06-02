import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))
from experience_composer import execute_experience_composer

def run_tests():
    print("=== RUNNING SKILL TESTS: EXPERIENCE-COMPOSER ===")
    test_input = {"example": "data"}
    try:
        result = execute_experience_composer(test_input)
        print("Result:", result)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    run_tests()
