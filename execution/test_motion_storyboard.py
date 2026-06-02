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

def test_motion_storyboard():
    print("=== MOTION STORYBOARD TEST START ===")
    
    tmp_dir = Path(".tmp/vision_test")
    tmp_dir.mkdir(parents=True, exist_ok=True)
    
    print("\n1. MOTION STORYBOARD ÜRETİLİYOR...")
    try:
        # Requesting image from openai/gpt-5.4-image-2
        prompt = "Create a UI motion design storyboard showing a dynamic scroll reveal animation for a luxury tech brand. The image must show 3 to 4 sequential keyframes side-by-side. Frame 1: element is invisible and shifted down. Frame 2: element is partially visible, moving up with motion trails/onion skinning. Frame 3: final resting state. Include UI animation annotations, directional arrows showing movement, and a cubic-bezier easing curve graph on the side. High detail, dark mode UI, technical blueprint aesthetic."
        
        img_response = client.chat.completions.create(
            model="openai/gpt-5.4-image-2", 
            messages=[{"role": "user", "content": prompt}],
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
        storyboard_path = tmp_dir / "storyboard.png"
        
        if image_url.startswith('data:image'):
            header, encoded = image_url.split(",", 1)
            storyboard_path.write_bytes(base64.b64decode(encoded))
        else:
            urllib.request.urlretrieve(image_url, storyboard_path)
            
        print(f"Storyboard kaydedildi: {storyboard_path}")

        print("\n2. STORYBOARD ANALİZ EDİLİYOR (GPT-4o)")
        image_b64 = base64.b64encode(storyboard_path.read_bytes()).decode()
        
        analysis_prompt = """
        You are an expert UI/UX Motion Designer AI. Analyze this motion design storyboard image and extract the animation properties.
        Look at the sequence of frames, the arrows, and any graphs.
        
        Extract a JSON object matching this schema:
        {
          "animation_type": "string (e.g. fade_in_up, slide_in_left, scale_up)",
          "initial_state": {
            "opacity": "number (0-1)",
            "y_offset": "string (e.g. '50px', '100%')"
          },
          "final_state": {
            "opacity": "number (0-1)",
            "y_offset": "string"
          },
          "easing_curve": "string (e.g. ease-out, cubic-bezier(0.25, 1, 0.5, 1), spring)",
          "pacing_feel": "string (e.g. snappy, smooth, cinematic)"
        }
        
        Output ONLY valid JSON, no explanations.
        """
        
        vision_response = client.chat.completions.create(
            model="openai/gpt-4o",
            messages=[{
                "role": "user",
                "content": [
                    {"type": "text", "text": analysis_prompt},
                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{image_b64}"}}
                ]
            }],
            max_tokens=1000
        )
        
        analysis_json = vision_response.choices[0].message.content.strip()
        print("Analiz Sonucu (JSON):")
        print(analysis_json)
        
        print("\n=== TEST BAŞARIYLA TAMAMLANDI ===")
        print(f"Lütfen üretilen görseli klasörden kontrol et: {tmp_dir.absolute()}")

    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"Test sırasında hata oluştu: {e}")

if __name__ == "__main__":
    test_motion_storyboard()
