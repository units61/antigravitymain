# -*- coding: utf-8 -*-
"""
ANDIP Vision-First Pipeline V2: 2-Stage Hybrid Prompt Templates.
Consolidates 5 stages into 2 mega-stages for faster, cheaper pipeline runs.

Stage A: Design Blueprint (Moodboard + Design Spec + Wireframe)
Stage B: Motion & Interaction (Hero Component + Motion Storyboard)
"""

# ==========================================
# STAGE A: DESIGN BLUEPRINT
# (Moodboard + Design Spec + Wireframe)
# ==========================================

STAGE_A_GENERATION = """Create a comprehensive, ultra-professional DESIGN BLUEPRINT panel for a premium website project.
Brand Concept: {brand_concept}

This single panel MUST contain THREE distinct zones arranged in a clean, readable layout:

ZONE 1 — MOODBOARD (Top-left quadrant):
- 3-4 high-end editorial photography samples capturing the brand mood, lighting, and texture
- Color harmony swatches showing 5-6 specific harmonious colors with VISIBLE HEX CODES printed next to each swatch
- Typography specimen: header font and body font examples with font names labeled
- Material/texture reference samples
- Overall mood: BRIGHT, VIBRANT, studio-quality, warm and inviting — NOT dark or moody

ZONE 2 — DESIGN TOKENS (Bottom-left quadrant):
- Typography hierarchy specimen: H1 (with px size), H2 (with px size), H3 (with px size), Body (with px size) — all annotated with exact sizes and line-heights
- Color palette blocks with PRECISE HEX CODES clearly written: background, foreground, accent, secondary accent, muted
- Component token previews: Button (Default, Hover states), Input field, Card component
- Border radius values, spacing grid units, shadow depth annotations
- All values must be LEGIBLE and READABLE

ZONE 3 — WIREFRAME (Right half):
- Full landing page wireframe showing 6 sections in a STORY SCROLL narrative layout:
  1. Hero section (full-viewport, bold statement)
  2. Story/About section (company narrative, who we are)
  3. Showcase/Product section (bento grid or gallery)
  4. Features/Differentiator section (what makes us different)
  5. Social proof/Testimonials (trust & community)
  6. CTA + Footer (call to action, sign-up)
- Each section clearly labeled with section name
- Grid column annotations (12-column hints)
- Content hierarchy indicators (visual weight)
- Layout style: Editorial storytelling, asymmetric composition, spacious sections

CRITICAL DESIGN DIRECTION:
- Use a LIGHT, BRIGHT color scheme — white or off-white backgrounds with vibrant accent colors
- Colors should be VIVID and LIVELY (coral, electric blue, warm orange, fresh green — NOT neon/dark/cyberpunk)
- The overall feel should be like a premium design studio portfolio — clean, sophisticated, warm
- Typography should be modern and elegant (serif + sans-serif pairing)
- Layout should feel like an editorial magazine — generous whitespace, beautiful imagery

Style: Clean professional design system presentation, bright theme, studio-quality grid layout.
Resolution: Ultra-sharp, highly detailed, every text annotation must be READABLE, 4k quality.
"""

STAGE_A_ANALYSIS = """You are an expert Design Intelligence AI. Analyze this Design Blueprint panel image and extract ALL design specifications from its three zones (Moodboard, Design Tokens, Wireframe) as a single structured JSON object.

Look carefully at:
- ZONE 1 (Moodboard): Extract brand mood, color swatches, typography style, texture feel
- ZONE 2 (Design Tokens): Extract EXACT hex codes, font sizes, border radius, spacing, shadow values
- ZONE 3 (Wireframe): Extract section order, layout types, content hierarchy, grid structure

Output ONLY valid JSON, starting with {{ and ending with }}, containing no explanations or markdown blocks.

JSON Schema:
{{
  "brand": {{
    "archetype": "string (e.g., Creator, Explorer, Sage, Lover, Ruler)",
    "name": "string (a creative brand name matching the DNA)",
    "energy_level": "integer (1-10)"
  }},
  "emotion": {{
    "primary": "string (e.g., vibrant, warm, professional, playful, elegant)",
    "secondary": ["string"],
    "visual_density": "string (clean | medium | dense)",
    "motion_energy": "integer (1-10)"
  }},
  "colors": {{
    "background": "string (hex code — should be light/bright)",
    "foreground": "string (hex code — dark text color)",
    "accent": "string (hex code — primary vivid accent)",
    "accent_hover": "string (hex code)",
    "secondary_accent": "string (hex code — secondary vivid color)",
    "muted": "string (hex code — subtle/muted tone)",
    "border": "string (hex code)",
    "card_bg": "string (hex code)"
  }},
  "typography": {{
    "header_font": "string (Google Font name, e.g. 'Playfair Display', 'DM Serif Display', 'Fraunces')",
    "body_font": "string (Google Font name, e.g. 'Inter', 'DM Sans', 'Plus Jakarta Sans')",
    "style_id": "string (e.g., editorial_serif, modern_geometric, classic_elegant)",
    "weight_contrast": "string (low | medium | high)",
    "font_sizes": {{
      "xs": "string (e.g. '0.75rem')",
      "sm": "string (e.g. '0.875rem')",
      "base": "string (e.g. '1rem')",
      "lg": "string (e.g. '1.125rem')",
      "xl": "string (e.g. '1.25rem')",
      "h3": "string (e.g. '1.875rem')",
      "h2": "string (e.g. '2.25rem')",
      "h1": "string (e.g. '3.75rem')"
    }},
    "font_weights": {{
      "normal": "string (e.g. '400')",
      "medium": "string (e.g. '500')",
      "semibold": "string (e.g. '600')",
      "bold": "string (e.g. '700')"
    }}
  }},
  "spatial": {{
    "density": "string (airy | balanced | dense)",
    "symmetry": "string (symmetric | asymmetric)",
    "depth_feeling": "string (flat | layered | immersive)"
  }},
  "border_radius": {{
    "sm": "string (e.g. '4px')",
    "md": "string (e.g. '8px')",
    "lg": "string (e.g. '16px')",
    "full": "string ('9999px')"
  }},
  "shadows": {{
    "sm": "string (CSS shadow)",
    "md": "string",
    "lg": "string"
  }},
  "spacing": {{
    "unit": "string (e.g. '4px')",
    "container_padding": "string (e.g. '2rem')"
  }},
  "ui_elements": {{
    "button_padding": "string (e.g. '0.75rem 1.5rem')",
    "button_border_radius": "string",
    "card_padding": "string (e.g. '1.5rem')",
    "card_border_radius": "string"
  }},
  "motion": {{
    "style": "string (cinematic | reactive | kinetic | minimal | elastic)",
    "pacing": "string (slow | medium | fast)"
  }},
  "interaction": {{
    "intensity": "integer (1-10)",
    "hover_style": "string (e.g., smooth_scale, soft_shadow, color_shift, gentle_lift)",
    "scroll_behavior": "string (e.g., story_reveal, parallax_narrative, smooth_stagger, section_fade)"
  }},
  "wireframe": {{
    "page_type": "string (e.g. landing_page, storytelling_page)",
    "layout_grid_type": "string (e.g., editorial_story, asymmetric, bento, vertical_stack)",
    "sections": [
      {{
        "id": "string (e.g. 'hero', 'story', 'showcase', 'features', 'testimonials', 'cta', 'footer')",
        "type": "string (e.g. hero | story_narrative | bento_showcase | split_feature | testimonial | cta | footer)",
        "visual_weight": "integer (1-10)",
        "layout_description": "string",
        "approximate_height": "string (e.g. '100vh', '80vh')",
        "content_elements": ["string"],
        "suggested_alignment": "string (left | center | split)"
      }}
    ]
  }}
}}
"""


# ==========================================
# STAGE B: MOTION & INTERACTION
# (Hero Component + Motion Storyboard)
# ==========================================

STAGE_B_GENERATION = """Create a professional UI MOTION & INTERACTION DESIGN PANEL for a premium storytelling website.
Brand Concept: {brand_concept}
Visual Style: {visual_style_description}
Brand Colors: Background {bg_color}, Accent {accent_color}, Secondary {secondary_accent}
Typography: {header_font} for headers, {body_font} for body
Page Sections: {sections_list}

This panel MUST contain TWO distinct zones:

ZONE 1 — HERO COMPONENT DETAIL (Left half):
- A HIGH-FIDELITY render of the hero section showing:
  1. Default/resting state — full pixel-level detail with perfect spacing, typography, and imagery
  2. Hover state overlay or side-by-side showing interactive changes (button glow, element shifts)
  3. Exact typographic treatment, padding, borders, and premium micro-details
- The hero should feel like an editorial magazine spread — bold headline, compelling imagery, warm inviting feel
- Use BRIGHT, VIBRANT colors — light background with vivid accents
- Show both desktop and key element close-ups

ZONE 2 — SCROLL STORY MOTION STORYBOARD (Right half):
- 3-4 sequential keyframe panels (Frame 1 → Frame 4) showing a STORY SCROLL reveal sequence:
  Frame 1 (Entry): Hero at rest, subtle ambient motion, content settled
  Frame 2 (Scroll Reveal): Hero slides up, story section parallax reveals with elements staggering in
  Frame 3 (Narrative Flow): Showcase section slides in horizontally, products/features appear with spring physics
  Frame 4 (Conclusion): Testimonials fade up, CTA pulses with warm glow, footer settles
- Motion annotations showing directional arrows and movement paths
- An annotated easing curve graph (cubic-bezier) on the side
- Physics parameters: spring constants, damping ratios, stagger timings
- Scroll trigger points annotated

CRITICAL DESIGN DIRECTION:
- All frames should use LIGHT, BRIGHT backgrounds — NOT dark mode
- Animations should feel ORGANIC and NARRATIVE — like turning pages of a beautiful story
- Transitions should be smooth, warm, and inviting — NOT aggressive or technical
- Story scroll: each section reveals like a new chapter
- Parallax depth should be subtle and elegant, not dramatic

Style: Technical UI/UX motion blueprint, bright/light theme, editorial quality, clean annotations.
Resolution: Sharp details, clear frame divisions, legible labels, 4k quality.
"""

STAGE_B_ANALYSIS = """You are an expert Motion Director and UI Engineer AI. Analyze this Motion & Interaction panel image and extract both the Hero component specifications AND the motion/animation physics as a single structured JSON object.

Look at:
- ZONE 1 (Hero Component): Extract layout, spacing, visual treatment, hover states, micro-interactions
- ZONE 2 (Motion Storyboard): Extract keyframe sequence, easing curves, spring physics, scroll triggers, stagger timing

Output ONLY valid JSON, starting with {{ and ending with }}, containing no explanations or markdown blocks.

JSON Schema:
{{
  "hero_component": {{
    "component_id": "string (e.g. 'hero_main')",
    "name": "string (human-readable name)",
    "visual_style": {{
      "layout": "string (e.g. 'flex-row', 'grid-cols-2', 'centered-stack')",
      "background_treatment": "string (e.g. 'warm gradient', 'clean white with accent overlays')",
      "border_style": "string",
      "padding": "string (e.g. '3rem 2rem')",
      "gap": "string (e.g. '2rem')"
    }},
    "states": {{
      "default": "string (detailed visual look of default state)",
      "hover": "string (hover transitions — scaling, color shifts, shadows)",
      "active": "string (active click state)"
    }},
    "interactivity": {{
      "cursor_type": "string (e.g. 'pointer')",
      "transition_duration": "string (e.g. '300ms')",
      "micro_interactions": ["string (e.g. 'gentle lift on hover', 'shadow deepen', 'text color shift')"]
    }}
  }},
  "motion": {{
    "animation_type": "string (e.g. 'story_scroll_narrative', 'parallax_chapter_reveal')",
    "initial_state": {{
      "opacity": "number (0-1)",
      "transform": "string (e.g. 'translateY(60px) scale(0.95)')"
    }},
    "final_state": {{
      "opacity": "number (0-1)",
      "transform": "string (e.g. 'translateY(0px) scale(1)')"
    }},
    "easing_curve": "string (e.g. 'cubic-bezier(0.22, 1, 0.36, 1)')",
    "duration": "string (e.g. '0.8s')",
    "pacing_feel": "string (e.g. 'warm-narrative', 'editorial-smooth', 'gentle-organic')",
    "spring_physics": {{
      "stiffness": "number (e.g. 200)",
      "damping": "number (e.g. 25)",
      "mass": "number (e.g. 1)"
    }},
    "scroll_trigger": {{
      "enabled": "boolean",
      "start_trigger": "string (e.g. 'top 80%')",
      "scrub": "boolean | number",
      "pin": "boolean"
    }},
    "stagger": {{
      "enabled": "boolean",
      "amount": "string (e.g. '0.12s')",
      "direction": "string (e.g. 'top-down', 'left-right', 'center-out')"
    }},
    "parallax": {{
      "enabled": "boolean",
      "layers": [
        {{
          "name": "string (e.g. 'foreground', 'midground', 'background')",
          "depth_offset": "string (e.g. '0px', '30px', '80px')",
          "speed": "number (e.g. 1.0, 0.7, 0.3)"
        }}
      ]
    }},
    "section_transitions": [
      {{
        "from_section": "string",
        "to_section": "string",
        "transition_type": "string (e.g. 'fade_slide_up', 'parallax_reveal', 'horizontal_slide')",
        "duration": "string"
      }}
    ]
  }}
}}
"""
