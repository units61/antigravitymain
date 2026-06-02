import sys
import json
from pathlib import Path

# Ensure the execution dir is in the Python path
sys.path.append(str(Path(__file__).parent))

from prompt_analyzer import analyze_prompt

test_prompts = [
    "Minimalist İskandinav tarzı bir mobilya mağazası, çok sakin hissettirmeli.",
    "Enerjik ve kaotik bir kripto para borsası, brutalist tasarım.",
    "Geleneksel ve güven veren bir kurumsal hukuk bürosu."
]

def run_tests():
    print("=== RUNNING SKILL TESTS: DESIGN DNA EXTRACTOR ===")
    for i, prompt in enumerate(test_prompts, 1):
        print(f"\n--- Test Case {i} ---")
        print(f"Prompt: {prompt}")
        print("Extracting DNA...")
        
        try:
            # We explicitly bypass cache for the test to see the live output 
            # Or we can use it to test the caching logic too. Let's use cache=False for testing accuracy.
            dna = analyze_prompt(prompt, use_cache=False)
            print("Result (JSON):")
            print(json.dumps(dna, indent=2, ensure_ascii=False))
        except Exception as e:
            print(f"Error during execution: {e}")
            
if __name__ == "__main__":
    run_tests()
