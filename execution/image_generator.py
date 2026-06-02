import os
import base64
import urllib.request
import re
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

def generate_image(prompt: str, save_path: Path, model: str = "openai/gpt-5.4-image-2") -> Path:
    """
    Generates a high-quality image using OpenRouter and saves it to the specified path.
    Strictly raises an exception on failure (No silent fallback).
    """
    if not OPENROUTER_API_KEY:
        raise ValueError("OPENROUTER_API_KEY is missing. Cannot generate images.")
        
    print(f"[IMAGE GEN] Requesting image for prompt: {prompt[:50]}...")
    
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=OPENROUTER_API_KEY,
    )
    
    # Adding quality markers to the prompt to enforce user preference #1
    quality_prompt = prompt + " High resolution, pristine quality, photorealistic or high-fidelity UI vector style as appropriate, 4k detail."
    
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": quality_prompt}],
        extra_body={"modalities": ["image"]},
        max_tokens=1000
    )
    
    message = response.choices[0].message
    image_url = ""
    msg_dict = message.model_dump()
    
    # Robust OpenRouter custom extra fields parsing (handles Pydantic v1 vs v2 extra fields and direct attribute access)
    images_list = getattr(message, "images", None)
    if not images_list and hasattr(message, "model_extra") and message.model_extra:
        images_list = message.model_extra.get('images')
    if not images_list:
        images_list = msg_dict.get('images')
    if not images_list and hasattr(response.choices[0], "model_extra") and response.choices[0].model_extra:
        c_extra = response.choices[0].model_extra
        if "message" in c_extra:
            m_val = c_extra["message"]
            if isinstance(m_val, dict):
                images_list = m_val.get("images")
            else:
                images_list = getattr(m_val, "images", None)
                
    # Parse OpenRouter image response formats
    if images_list:
        if isinstance(images_list, list) and len(images_list) > 0:
            first_image = images_list[0]
            if isinstance(first_image, dict) and 'image_url' in first_image:
                image_url = first_image['image_url'].get('url', '')
            elif hasattr(first_image, 'image_url'):
                image_url = first_image.image_url.url
                
    content = getattr(message, "content", None) or msg_dict.get('content')
    if not image_url and content:
        if isinstance(content, str) and 'http' in content:
            urls = re.findall(r'(https?://[^\s\)]+)', content)
            if urls:
                image_url = urls[0]
        elif isinstance(content, list):
            for block in content:
                if isinstance(block, dict):
                    if block.get('type') == 'image_url':
                        image_url = block.get('image_url', {}).get('url', '')
                    elif block.get('type') == 'image':
                        image_url = block.get('image', '')
                        
    if not image_url:
        err_ctx = {
            "msg_dict": msg_dict,
            "model_extra": getattr(message, "model_extra", None),
            "choice_extra": getattr(response.choices[0], "model_extra", None)
        }
        raise RuntimeError(f"Failed to extract image URL from response. Details: {err_ctx}")
        
    # Ensure parent directory exists
    save_path.parent.mkdir(parents=True, exist_ok=True)
    
    if image_url.startswith('data:image'):
        header, encoded = image_url.split(",", 1)
        save_path.write_bytes(base64.b64decode(encoded))
    else:
        urllib.request.urlretrieve(image_url, save_path)
        
    print(f"[IMAGE GEN SUCCESS] Saved to {save_path}")
    return save_path

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 2:
        generate_image(sys.argv[1], Path(sys.argv[2]))
    else:
        print("Usage: python image_generator.py <prompt> <output_path>")
