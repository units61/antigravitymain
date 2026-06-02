import os
import json
import base64
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
)

def test_vision_pipeline():
    print("=== VISION PIPELINE TEST START ===")
    prompt = "Luxury cyberpunk fragrance brand for Gen Z. Dark neon, high-end, mysterious."
    
    tmp_dir = Path(".tmp/vision_test")
    tmp_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"\n1. MOODBOARD ÜRETİLİYOR (Prompt: {prompt})")
    try:
        img_response = client.chat.completions.create(
            model="openai/gpt-5.4-image-2", 
            messages=[{"role": "user", "content": f"Create a professional creative moodboard for a web design project. Brand concept: {prompt}. The moodboard should include: Atmospheric photography samples showing the desired mood/energy, Color harmony swatches (4-6 colors), Typography specimens, Material/texture references. Style: Dark background, editorial grid layout, high-end design studio aesthetic. High detail, crisp, professional quality."}],
            extra_body={"modalities": ["image"]},
            max_tokens=1000
        )
        
        message = img_response.choices[0].message
        image_url = ""
        
        msg_dict = message.model_dump()
        
        if msg_dict.get('images'):
            images_list = msg_dict['images']
            if isinstance(images_list, list) and len(images_list) > 0:
                first_image = images_list[0]
                if isinstance(first_image, dict) and 'image_url' in first_image:
                    image_url = first_image['image_url'].get('url', '')
                elif hasattr(first_image, 'image_url'):
                    image_url = first_image.image_url.url
        
        if not image_url and msg_dict.get('content'):
            content = msg_dict['content']
            if isinstance(content, str) and 'http' in content:
                import re
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
             print("Görsel URL'si çıkartılamadı.")
             return
             
        print(f"Görsel üretildi: {image_url[:50]}...")
        
        import urllib.request
        moodboard_path = tmp_dir / "moodboard.png"
        
        if image_url.startswith('data:image'):
            header, encoded = image_url.split(",", 1)
            moodboard_path.write_bytes(base64.b64decode(encoded))
        else:
            urllib.request.urlretrieve(image_url, moodboard_path)
            
        print(f"Moodboard kaydedildi: {moodboard_path}")

        print("\n2. MOODBOARD ANALİZ EDİLİYOR (GPT-4o)")
        image_b64 = base64.b64encode(moodboard_path.read_bytes()).decode()
        
        vision_response = client.chat.completions.create(
            model="openai/gpt-4o",
            messages=[{
                "role": "user",
                "content": [
                    {"type": "text", "text": "You are an expert Design Intelligence AI. Analyze this moodboard image and extract the design DNA as a structured JSON object. Extract: {\"brand_energy\": 1-10, \"emotion\": {\"primary\": \"string\", \"visual_density\": \"clean|medium|dense\"}, \"colors\": {\"background\": \"#hex\", \"foreground\": \"#hex\", \"accent\": \"#hex\"}, \"typography\": {\"header_font_suggestion\": \"string\"}}. Output ONLY valid JSON, no explanations."},
                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{image_b64}"}}
                ]
            }],
            max_tokens=1000
        )
        
        analysis_json = vision_response.choices[0].message.content.strip()
        print("Analiz Sonucu (JSON):")
        print(analysis_json)
        
        print("\n=== TEST BAŞARIYLA TAMAMLANDI ===")
        print(f"Lütfen üretilen görselleri klasörden kontrol et: {tmp_dir.absolute()}")

    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"Test sırasında hata oluştu: {e}")

if __name__ == "__main__":
    test_vision_pipeline()
