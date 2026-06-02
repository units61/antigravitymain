import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))
from ontology_manager import execute_ontology_manager

def run_tests():
    print("=== RUNNING SKILL TESTS: ONTOLOGY-MANAGER ===")
    test_input = {"example": "data"}
    try:
        result = execute_ontology_manager(test_input)
        print("Result:", result)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    run_tests()
