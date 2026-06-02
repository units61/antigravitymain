import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))
from motion_director import execute_motion_director

def run_tests():
    print("=== RUNNING SKILL TESTS: MOTION-DIRECTOR ===")
    test_input = {"example": "data"}
    try:
        result = execute_motion_director(test_input)
        print("Result:", result)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    run_tests()
