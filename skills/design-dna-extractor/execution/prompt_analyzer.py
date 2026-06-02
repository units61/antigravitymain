import os
import json
import hashlib
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

def get_directive() -> str:
    """Reads the prompt-understanding directive."""
    directive_path = Path(__file__).parent.parent / "SKILL.md"
    if not directive_path.exists():
        raise FileNotFoundError(f"Directive not found at {directive_path}")
    return directive_path.read_text(encoding="utf-8")

def analyze_prompt(user_prompt: str, use_cache: bool = True) -> dict:
    """
    Analyzes a user prompt and returns the Design DNA JSON.
    Uses caching to minimize token usage.
    """
    # Setup cache directory
    tmp_dir = Path(__file__).parent.parent / ".tmp" / "cache"
    tmp_dir.mkdir(parents=True, exist_ok=True)
    
    # Check cache
    prompt_hash = hashlib.md5(user_prompt.encode("utf-8")).hexdigest()
    cache_file = tmp_dir / f"dna_{prompt_hash}.json"
    
    if use_cache and cache_file.exists():
        print(f"[CACHE HIT] Returning cached Design DNA for prompt: '{user_prompt[:30]}...'")
        return json.loads(cache_file.read_text(encoding="utf-8"))
    
    # If no cache, call LLM
    print(f"[API CALL] Analyzing prompt: '{user_prompt[:30]}...'")
    
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=OPENROUTER_API_KEY,
    )
    
    system_prompt = get_directive()
    
    response = client.chat.completions.create(
        model="anthropic/claude-3-haiku", # Using Haiku via OpenRouter
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": f"Analyze this request and output the Design DNA JSON:\n\n{user_prompt}"
            }
        ]
    )
    
    raw_output = response.choices[0].message.content.strip()
    
    # Basic cleanup in case the LLM wrapped it in markdown blocks
    if raw_output.startswith("```json"):
        raw_output = raw_output[7:]
    if raw_output.startswith("```"):
        raw_output = raw_output[3:]
    if raw_output.endswith("```"):
        raw_output = raw_output[:-3]
        
    try:
        dna_json = json.loads(raw_output.strip())
        # Save to cache
        cache_file.write_text(json.dumps(dna_json, indent=2, ensure_ascii=False), encoding="utf-8")
        return dna_json
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON from LLM: {e}")
        print(f"Raw Output:\n{raw_output}")
        raise

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        prompt = sys.argv[1]
        print(json.dumps(analyze_prompt(prompt), indent=2))
    else:
        print("Usage: python prompt_analyzer.py <your_prompt>")
