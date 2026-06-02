# -*- coding: utf-8 -*-
"""
Quick test runner for the V2 (2-stage hybrid) Vision Pipeline.
Usage: python -m execution.test_vision_pipeline_v2
       python -m execution.test_vision_pipeline_v2 "your custom prompt here"
"""

import sys
import json
from pathlib import Path

# Setup paths
BASE_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(BASE_DIR))

from execution.vision_pipeline_v2 import run_vision_pipeline_v2

def main():
    prompt = "A premium creative studio storytelling landing page with vibrant colors, warm editorial feel, and story scroll narrative."
    
    if len(sys.argv) > 1:
        prompt = sys.argv[1]
    
    print(f"\n{'='*60}")
    print(f"TESTING VISION PIPELINE V2 (2-STAGE HYBRID)")
    print(f"Prompt: {prompt}")
    print(f"{'='*60}\n")
    
    blueprint = run_vision_pipeline_v2(prompt)
    
    # Print summary
    print(f"\n{'='*60}")
    print(f"V2 PIPELINE TEST RESULTS")
    print(f"{'='*60}")
    print(f"Session: {blueprint['metadata']['session_id']}")
    print(f"Visual assets generated: {list(blueprint['visual_assets'].keys())}")
    print(f"Brand name: {blueprint['design_dna'].get('brand', {}).get('name', 'N/A')}")
    print(f"Colors BG: {blueprint['visual_language']['color_tokens'].get('background', 'N/A')}")
    print(f"Colors Accent: {blueprint['visual_language']['color_tokens'].get('primary_accent', 'N/A')}")
    print(f"Header font: {blueprint['visual_language']['typography_tokens'].get('header_font', 'N/A')}")
    print(f"Body font: {blueprint['visual_language']['typography_tokens'].get('body_font', 'N/A')}")
    print(f"Sections: {[s.get('id') for s in blueprint['experience_flow'].get('sections', [])]}")
    print(f"Motion easing: {blueprint['motion_graph'].get('global_motion', {}).get('easing_curve', 'N/A')}")
    print(f"Critic score: {blueprint['critique_report'].get('overall_score', 'N/A')}")
    print(f"{'='*60}\n")

if __name__ == "__main__":
    main()
