import sys
import json
from pathlib import Path

sys.path.append(str(Path(__file__).parent))

from prompt_analyzer import analyze_prompt
from ontology_engine import resolve_design_dna

# 10 diverse, complex prompts representing different archetypes, emotions, and designs
test_prompts = [
    # 1. Luxury Boutique Fashion
    "A highly elite, luxury digital boutique for an avant-garde French fashion house. Extremely slow cinematic reveals, gold accents, spacious margins, premium serif typography.",
    # 2. Cyberpunk Crypto Exchange
    "A chaotic and energetic crypto derivatives exchange for Gen-Z traders. Brutalist grid layouts, hyper-neon green accents on absolute black, highly kinetic motion, technical monospace fonts.",
    # 3. Organic Herbal Tea Brand
    "A calming, sustainable organic herbal tea brand. Warm botanical earth colors, soft pastel layouts, outfit sans-serif typography, gentle fluid spring interactions.",
    # 4. Modern B2B SaaS Platform
    "A clean, professional and highly trustworthy corporate B2B SaaS platform for enterprise workflow management. Structured grid columns, modern geometric blue branding, minimal fast animations.",
    # 5. Playful Kids Toy Brand
    "A colorful, friendly and highly playful learning toy brand for toddlers. Energetic bouncy spring cards, rounded friendly fonts, bright pop colors, elastic cursor ripples.",
    # 6. Editorial Architecture Journal
    "A high-end architectural portfolio and editorial journal. Heavy asymmetrical layout grids, monochrome minimalist palettes, luxury editorial serif typography, slow fade transitions.",
    # 7. Cinematic Sci-Fi Game Promo
    "A mysterious and immersive landing page for a sci-fi space simulation game. Cinematic space backdrop, slow-burn reveals, dark purple velvet palettes, custom magnetic cursor elements.",
    # 8. Disruptive Streetwear Label
    "A bold and rebellious streetwear brand. High-contrast raw industrial grids, aggressive heavy margins, bright safety yellow accents, industrial monospace fonts.",
    # 9. Wholesome Wellness Clinic
    "An innocent, welcoming wellness clinic focusing on gentle mental health care. Extremely serene and clean layouts, soft pastel calming colors, light sans fonts, minimal fade animations.",
    # 10. Futuristic Tech Venture
    "An avant-garde deep-tech venture studio. Highly structural grid rules, dark mysterious aesthetics, Space Grotesk mechanical font pairings, reactive magnetic elements."
]

def run_e2e_tests():
    print("==================================================")
    print("   ANDIP PHASE 1: END-TO-END SYSTEM EVALUATION    ")
    print("==================================================\n")
    
    success_count = 0
    total_count = len(test_prompts)
    
    # Ensure cache is active for tests to avoid hitting OpenRouter unnecessarily,
    # but still execute live when required.
    for i, prompt in enumerate(test_prompts, 1):
        print(f"[{i}/{total_count}] Processing: '{prompt[:60]}...'")
        try:
            # Step A: Run Prompt Analyzer -> Extract Design DNA
            dna = analyze_prompt(prompt, use_cache=True)
            # Add prompt hint
            dna["prompt_hint"] = prompt
            
            # Step B: Run Ontology Engine -> Resolve concrete tokens and apply Graph Rules
            tokens = resolve_design_dna(dna)
            
            # Step C: Assertions & Validations
            assert "brand" in tokens, "Missing brand profile"
            assert "emotion" in tokens, "Missing emotion profile"
            assert "colors" in tokens, "Missing color palette"
            assert "typography" in tokens, "Missing typography style"
            assert "spatial" in tokens, "Missing spatial mode"
            assert "motion" in tokens, "Missing motion profile"
            assert "interaction" in tokens, "Missing interaction model"
            assert "selected_pattern" in tokens, "Missing selected pattern"
            
            print(f" -> SUCCESS: Resolved to brand: {tokens['brand']['name']}, emotion: {tokens['emotion']['id']}")
            print(f"    - Colors: {tokens['colors']['palette_name']} ({tokens['colors']['accent']})")
            print(f"    - Typography: {tokens['typography']['header_font']} / {tokens['typography']['body_font']}")
            print(f"    - Spatial Mode: {tokens['spatial']['mode_name']} (density: {tokens['emotion']['visual_density']})")
            print(f"    - Motion Config: {tokens['motion']['style_name']} ({tokens['motion']['type']})")
            print(f"    - Best Pattern Selected: '{tokens['selected_pattern']['name']}'")
            
            # Print corrections if any
            if tokens["metadata"]["applied_corrections"]:
                print(f"    - [CORRECTIONS APPLIED]:")
                for corr in tokens["metadata"]["applied_corrections"]:
                    print(f"      * {corr['message']}")
            if tokens["metadata"]["applied_warnings"]:
                print(f"    - [WARNINGS APPLIED]:")
                for warn in tokens["metadata"]["applied_warnings"]:
                    print(f"      * {warn['message']}")
            print("-" * 50)
            success_count += 1
            
        except Exception as e:
            print(f" -> FAILED at step {i}: {e}")
            print("-" * 50)
            
    print(f"\n==================================================")
    print(f"   EVALUATION COMPLETE: {success_count}/{total_count} PASSED")
    print(f"==================================================")
    
    if success_count == total_count:
        print("\nAll systems operational. Design Brain Phase 1 is officially complete and certified.")
        return True
    else:
        print("\nSome tests failed. Check logs and self-anneal.")
        return False

if __name__ == "__main__":
    run_e2e_tests()
