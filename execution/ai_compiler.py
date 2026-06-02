import os
import json
import re
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

def get_code_generation_directive() -> str:
    """Reads the Next.js + TailwindCSS Code Generation SOP directive."""
    directive_path = Path(__file__).parent.parent / "directives" / "code-generation.md"
    if not directive_path.exists():
        return "You are an AI frontend compiler. Write premium, responsive, accessible Next.js + Tailwind CSS React components."
    return directive_path.read_text(encoding="utf-8")

def compile_component_from_scratch(
    comp_id: str,
    section_data: dict,
    visual_language: dict,
    design_dna: dict,
    motion_graph: dict = None,
    model: str = "anthropic/claude-sonnet-4.5",
    vision_ref: str = None
) -> str:
    """
    Calls OpenRouter LLM to write a 100% custom, from-scratch, premium React JSX component
    tailored specifically to the customer's visual language and experience flow.
    Supports vision references for multimodal visual-to-code generation.
    """
    print(f"[AI COMPILER] Sentezleniyor: '{comp_id}' sıfırdan yazılıyor ({model})...")
    
    if not OPENROUTER_API_KEY:
        print("[AI COMPILER WARNING] OPENROUTER_API_KEY missing. Cannot perform scratch compilation.")
        return ""
        
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=OPENROUTER_API_KEY,
    )
    
    directive = get_code_generation_directive()
    
    # Construct a highly specialized instruction set for from-scratch code synthesis
    system_prompt = f"""{directive}

CRITICAL ASSIGNMENT:
You are the "AI Compiler" inside the Infinite Possibility Engine. You do NOT use templates.
You must compile a 100% unique, premium, production-ready React (JSX) component named precisely `{comp_id}`.
It must match the customer's precise creative vision and layout details.

THE ARCHITECTURE & DESIGN SYSTEM RULES:
1. Start with `"use client";` at the very first line of the file.
2. Use Lucide icons: `import {{ ... }} from 'lucide-react';` if you need icons.
3. Use Framer Motion: `import {{ motion, AnimatePresence }} from 'framer-motion';` for animations.
4. Bridge the global visual system tokens perfectly:
   - Use dynamic colors: `background` -> `bg-background`, `foreground` -> `text-foreground`, `accent` -> `text-accent` / `bg-accent` / `border-accent`, `muted` -> `text-muted`.
   - Use dynamic borders: `border-custom` (radius), `border-custom` (width).
   - Use dynamic fonts: `font-header` for headings, `font-body` for body text.
5. High Contrast compliance: Ensure all text elements are highly readable against their background colors.
6. Responsive Layout: Build elegant padding and margins using `clamp()` or Tailwind utility breakpoints (`sm:`, `md:`, `lg:`).
7. Keyboard Focus: Add `focus-visible:ring-2 focus-visible:ring-accent outline-none` to all interactive buttons or inputs.
8. Animations: Make the component feel alive with subtle micro-animations (e.g. spring hover states, scroll-bound fades).

OUTPUT FORMATTING RULE:
- Output ONLY the clean, valid React component code.
- Absolutely NO markdown text, NO chat, NO explanations, NO surrounding text.
- Do NOT wrap code in ```jsx or ``` blocks, just output the raw code directly.
"""

    has_vision = False
    if vision_ref:
        image_path = Path(vision_ref)
        if image_path.exists():
            has_vision = True
            if model in ["anthropic/claude-3-haiku", "anthropic/claude-3.5-sonnet", "anthropic/claude-sonnet-latest", "anthropic/claude-sonnet-4.5"] or not model:
                # Upgrade to the world's most advanced multimodal frontend compiler model
                model = "anthropic/claude-sonnet-4.5"
                
    if has_vision:
        import base64
        image_path = Path(vision_ref)
        print(f"[AI COMPILER] Visual reference found: {image_path.name}. Performing multimodal compilation using {model}...")
        image_b64 = base64.b64encode(image_path.read_bytes()).decode()
        
        user_message_content = [
            {
                "type": "text",
                "text": f"""Customer Design DNA:
{json.dumps(design_dna, indent=2)}

Art Director's Visual System:
{json.dumps(visual_language, indent=2)}

Component Specifications & Copywriting:
{json.dumps(section_data, indent=2)}

Motion Graph Parameters:
{json.dumps(motion_graph, indent=2) if motion_graph else "{{}}"}

Write the complete code for the React component `<{comp_id} />`.
The component function signature must look exactly like this:
export default function {comp_id}({{ title, subtitle, eyebrow, colors, items, primary_cta, motion_config }})

CRITICAL VISUAL COMPILER REQUIREMENT:
You are provided with a high-fidelity visual render of the component in the attached image.
Analyze this visual representation extremely carefully.
Your task is to write Next.js React and Tailwind CSS code that replicates the exact layout structure, typography treatment, spacing, border styles, shadows, alignments, and aesthetic elements shown in the image as closely as possible.
Ensure that it is 100% robust, handles empty/undefined props gracefully, styles every element with Tailwind and inline custom CSS vars if needed, and is wowed-at-first-glance premium.
"""
            },
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/png;base64,{image_b64}",
                    "detail": "high"
                }
            }
        ]
    else:
        user_message_content = f"""Customer Design DNA:
{json.dumps(design_dna, indent=2)}

Art Director's Visual System:
{json.dumps(visual_language, indent=2)}

Component Specifications & Copywriting:
{json.dumps(section_data, indent=2)}

Motion Graph Parameters:
{json.dumps(motion_graph, indent=2) if motion_graph else "{{}}"}

Write the complete code for the React component `<{comp_id} />`.
The component function signature must look exactly like this:
export default function {comp_id}({{ title, subtitle, eyebrow, colors, items, primary_cta, motion_config }})

Ensure that it is 100% robust, handles empty/undefined props gracefully, styles every element with Tailwind and inline custom CSS vars if needed, and is wowed-at-first-glance premium.
"""

    try:
        messages = [
            {"role": "system", "content": system_prompt}
        ]
        if isinstance(user_message_content, list):
            messages.append({"role": "user", "content": user_message_content})
        else:
            messages.append({"role": "user", "content": user_message_content})

        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.2
        )
        
        raw_code = response.choices[0].message.content.strip()
        
        # Clean up any accidental code blocks outputted by the model
        if raw_code.startswith("```"):
            lines = raw_code.splitlines()
            if lines[0].startswith("```"):
                lines = lines[1:]
            if lines and lines[-1].startswith("```"):
                lines = lines[:-1]
            raw_code = "\n".join(lines).strip()
            
        # Ensure it has use client directive
        if not raw_code.startswith('"use client"') and not raw_code.startswith("'use client'"):
            raw_code = '"use client";\n\n' + raw_code
            
        print(f"[AI COMPILER SUCCESS] Generated {len(raw_code.splitlines())} lines of custom JSX code for '{comp_id}'.")
        return raw_code
        
    except Exception as e:
        print(f"[AI COMPILER ERROR] Failed scratch compilation for component '{comp_id}': {e}")
        return ""

if __name__ == "__main__":
    # Small test compilation run
    sample_dna = {"brand": {"name": "Lüks Zeytinyağı"}}
    sample_visual = {"color_tokens": {"background": "#FFF7F2", "foreground": "#1c1917", "primary_accent": "#ffa27c"}}
    sample_section = {
        "title": "AIONA",
        "description": "1200 yıllık bilge esans.",
        "resolved_props": {
            "title": "AIONA",
            "subtitle": "Asırlık ağaçlar",
            "items": [{"title": "Saflık", "description": "0.12 asitlik"}]
        }
    }
    
    code = compile_component_from_scratch("TestComponent", sample_section, sample_visual, sample_dna)
    print(code[:300] + "\n...")
