import os
import json
import base64
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

def analyze_image(image_path: Path, analysis_prompt: str, model: str = "openai/gpt-4o") -> dict:
    """
    Analyzes an image using Vision AI and extracts structured JSON data.
    If the selected model fails or returns a refusal (safety trigger), automatically
    falls back to alternative models (e.g., google/gemini-2.5-flash, anthropic/claude-3.5-sonnet).
    """
    if not OPENROUTER_API_KEY:
        raise ValueError("OPENROUTER_API_KEY is missing. Cannot perform vision analysis.")
        
    if not image_path.exists():
        raise FileNotFoundError(f"Image not found at {image_path}")
        
    # Order of fallback models to maximize safety-bypass and JSON quality
    fallback_models = [model, "google/gemini-2.5-flash", "anthropic/claude-3.5-sonnet"]
    # Ensure no duplicates
    models_to_try = []
    for m in fallback_models:
        if m not in models_to_try:
            models_to_try.append(m)

    last_error = None
    image_b64 = base64.b64encode(image_path.read_bytes()).decode()
    
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=OPENROUTER_API_KEY,
    )

    for current_model in models_to_try:
        print(f"[VISION AI] Attempting analysis on {image_path.name} using {current_model}...")
        try:
            response = client.chat.completions.create(
                model=current_model,
                messages=[{
                    "role": "user",
                    "content": [
                        {"type": "text", "text": analysis_prompt},
                        {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{image_b64}", "detail": "high"}}
                    ]
                }],
                max_tokens=2000
            )
            
            raw_output = response.choices[0].message.content.strip()
            
            # Check for safety refusals or empty responses
            if not raw_output or any(refusal in raw_output.lower() for refusal in ["i'm sorry", "i cannot assist", "i can't assist", "unable to analyze"]):
                print(f"[VISION AI WARN] Model {current_model} returned safety refusal/empty response. Retrying with next model...")
                last_error = RuntimeError(f"Safety refusal or empty response from {current_model}: {raw_output[:100]}")
                continue

            # Clean markdown json blocks
            cleaned = raw_output
            if cleaned.startswith("```json"):
                cleaned = cleaned[7:]
            if cleaned.startswith("```"):
                cleaned = cleaned[3:]
            if cleaned.endswith("```"):
                cleaned = cleaned[:-3]
            cleaned = cleaned.strip()

            data = json.loads(cleaned)
            print(f"[VISION AI SUCCESS] Extracted {len(data.keys())} top-level keys using {current_model}.")
            return data

        except json.JSONDecodeError as e:
            print(f"[VISION AI WARN] JSON decode failed for model {current_model}. Output was:\n{raw_output[:300]}...")
            last_error = RuntimeError(f"JSONDecodeError with {current_model}: {e}")
            continue
        except Exception as e:
            print(f"[VISION AI WARN] Model {current_model} failed with exception: {e}")
            last_error = e
            continue

    # If all models failed, raise the final error
    raise RuntimeError(f"All vision fallback models failed. Last error: {last_error}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 2:
        print(json.dumps(analyze_image(Path(sys.argv[1]), sys.argv[2]), indent=2))
    else:
        print("Usage: python vision_analyzer.py <image_path> <prompt>")
