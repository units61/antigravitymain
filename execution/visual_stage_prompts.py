# -*- coding: utf-8 -*-
"""
ANDIP Visual-First Pipeline: Stage-Specific Prompt Templates for Image Generation and Vision Analysis.
This module houses the prompt templates and corresponding JSON schemas for all 5 stages of the pipeline.
"""

# ==========================================
# STAGE 1: MOODBOARD
# ==========================================

MOODBOARD_GENERATION = """Create a professional, highly curated creative moodboard collage for a web design project.
Brand concept: {brand_concept}

The moodboard MUST contain:
1. Atmospheric high-end photography samples capturing the emotional DNA, mood, lighting, and texture.
2. Color harmony swatches showing 4 to 6 specific, harmonious colors.
3. Typography specimen headers and body texts displaying visual contrast.
4. Material, textile, or surface texture references.
5. Subtle spatial grid alignments.

Style: Dark premium editorial grid layout, professional creative studio aesthetic, clean presentation.
Resolution: Ultra-sharp, highly detailed, visually stunning, 4k quality. NO text placeholders like lorem ipsum outside of beautiful type specimens. Do not use generic icons. Make it look like a real Pinterest or Figma design studio moodboard.
"""

MOODBOARD_ANALYSIS = """You are an expert Design Intelligence AI. Analyze this brand moodboard image and extract the design DNA as a structured JSON object matching the schema below.
Look at the atmospheric visuals, typography specimens, color swatches, and layouts to extract precise design properties.

Output ONLY valid JSON, starting with {{ and ending with }}, containing no explanations or markdown blocks.

JSON Schema:
{{
  "brand": {{
    "archetype": "string (e.g., Outlaw, Ruler, Creator, Lover, Sage, Explorer, Magician, Jester, Citizen, Caregiver, Hero, Innocent)",
    "name": "string (a creative concept name matching this DNA)",
    "energy_level": "integer (1-10, where 1 is static/calm, 10 is explosive/chaotic)"
  }},
  "emotion": {{
    "primary": "string (e.g., luxury, rebellion, calm, corporate, tech, futuristic, organic)",
    "secondary": ["string"],
    "visual_density": "string (clean | medium | dense)",
    "motion_energy": "integer (1-10, representing speed/energy expected in movement)"
  }},
  "colors": {{
    "background": "string (exact dominant hex color, e.g. '#0b0c10')",
    "foreground": "string (exact readable content hex color, e.g. '#ffffff')",
    "accent": "string (exact vivid highlight hex color, e.g. '#ff007f')",
    "muted": "string (exact subtle tone hex color, e.g. '#66fcf1')"
  }},
  "typography": {{
    "style_id": "string (e.g., classic_serif, ultra_brutalist, neo_grotesque, monospace, organic_script)",
    "header_font_suggestion": "string (Google Font name, e.g. 'Cinzel', 'Syne', 'Playfair Display', 'Inter', 'Space Grotesk')",
    "body_font_suggestion": "string (Google Font name, e.g. 'Inter', 'Montserrat', 'Lora', 'Space Mono')",
    "weight_contrast": "string (low | medium | high)"
  }},
  "spatial": {{
    "density": "string (airy | balanced | dense)",
    "symmetry": "string (symmetric | asymmetric)",
    "depth_feeling": "string (flat | layered | immersive)"
  }},
  "motion": {{
    "style": "string (cinematic | reactive | kinetic | minimal | elastic)",
    "pacing": "string (slow | medium | fast)"
  }},
  "interaction": {{
    "intensity": "integer (1-10)",
    "hover_style": "string (e.g. magnetic_grow, fluid_underline, border_glow, skew_reveal)",
    "scroll_behavior": "string (e.g. parallax_reveal, bento_stagger, smooth_momentum, spring_bounce)"
  }}
}}
"""


# ==========================================
# STAGE 2: DESIGN SPECS
# ==========================================

DESIGN_SPECS_GENERATION = """Create a modern and highly technical Design System Specification Sheet or Style Guide.
Brand Concept: {brand_concept}
Design DNA:
- Primary Emotion: {primary_emotion}
- Color Palette suggestion: {bg_color} (bg), {fg_color} (fg), {accent_color} (accent)
- Typography Style: {header_font} (Header), {body_font} (Body)

The spec sheet MUST show a high-fidelity visual layout containing:
1. Palette blocks displaying primary, secondary, accent, and muted tones with precise Hex codes written next to them.
2. Typography hierarchy specimen displaying H1, H2, H3, and Body with font sizes and line heights annotated.
3. Component token previews showcasing buttons (Default, Hover, Disabled), Inputs, and Card components.
4. Micro-tokens like border radius curves, shadow depth layers, and spacing grids.

Style: Technical blueprint grid style, high-end design token UI, dark mode, precise annotations.
Resolution: Pristine, clean vector-like crispness, 4k detail. Every detail must look realistic and readable.
"""

DESIGN_SPECS_ANALYSIS = """You are an expert Frontend Architect AI. Parse this Design System Specification Sheet image and extract the exact values as a structured JSON object matching the schema below.
Analyze the color swatches, typography sizes, border radiuses, shadows, and spacing annotations to extract real design tokens.

Output ONLY valid JSON, starting with {{ and ending with }}, containing no explanations or markdown blocks.

JSON Schema:
{{
  "colors": {{
    "background": "string (hex code)",
    "foreground": "string (hex code)",
    "accent": "string (hex code)",
    "accent_hover": "string (hex code)",
    "muted": "string (hex code)",
    "border": "string (hex code)",
    "card_bg": "string (hex code)"
  }},
  "typography": {{
    "header_font": "string (Google Font suggestion based on image visual style)",
    "body_font": "string (Google Font suggestion based on image)",
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
  "border_radius": {{
    "none": "string (0px)",
    "sm": "string (e.g. '4px')",
    "md": "string (e.g. '8px')",
    "lg": "string (e.g. '16px')",
    "full": "string (9999px)"
  }},
  "shadows": {{
    "none": "string",
    "sm": "string (CSS shadow representation)",
    "md": "string",
    "lg": "string"
  }},
  "spacing": {{
    "unit": "string (e.g., '4px')",
    "container_padding": "string (e.g., '2rem')"
  }},
  "ui_elements": {{
    "button_padding": "string (e.g., '0.75rem 1.5rem')",
    "button_border_radius": "string",
    "card_padding": "string (e.g., '1.5rem')",
    "card_border_radius": "string"
  }}
}}
"""


# ==========================================
# STAGE 3: WIREFRAME
# ==========================================

WIREFRAME_GENERATION = """Create a high-fidelity website landing page wireframe that dictates the layout structure.
Brand Concept: {brand_concept}
Design Aesthetics:
- Primary theme: {primary_emotion}
- Color DNA: {accent_color} accents on {bg_color} background
- Typography suggestion: {header_font} and {body_font}

The wireframe MUST show a full landing page structure containing:
1. Clear block layout sections (Hero, Bento showcase, Split Features, Intersecting grids, CTA, and Footer).
2. Wireframe elements showing content hierarchy, visual weights, spatial containers, and layout grids.
3. Explicit layout structure (e.g., asymmetric grid, overlapping layers, rigid geometric containers, fluid spacious sections).
4. Interface annotations pointing out section boundaries and grid column alignments (12-column layout hints).

Style: Clean technical UI wireframe, editorial composition, high contrast layout, wireframe annotations.
Resolution: Crisp lines, readable block shapes, high resolution, 4k quality.
"""

WIREFRAME_ANALYSIS = """You are an expert UX Architect AI. Analyze this website landing page wireframe and extract the full page layout structure as a structured JSON object matching the schema below.
Identify the grid layout types, section orders, visual weights, alignments, and specific UI elements.

Output ONLY valid JSON, starting with {{ and ending with }}, containing no explanations or markdown blocks.

JSON Schema:
{{
  "page_type": "string (e.g. landing_page)",
  "layout_grid_type": "string (e.g. bento, symmetric_grid, split_screen, raw_minimal, vertical_stack, asymmetric)",
  "sections": [
    {{
      "id": "string (e.g., 'hero', 'bento_showcase', 'split_feature', 'gallery_grid', 'cta_banner', 'footer')",
      "type": "string (e.g. hero | bento_showcase | split_feature | stats_grid | testimonial | cta | footer)",
      "visual_weight": "integer (1-10, representing visual dominance where 10 is highest)",
      "layout_description": "string (e.g. 'Asymmetric 3-column bento box', 'Split screen with large typography on left and interactive card on right')",
      "approximate_height": "string (e.g. '100vh', '600px')",
      "content_elements": ["string (e.g. 'H1 Title', 'Explosive magnetic CTA button', 'Background 3D Canvas element')"],
      "suggested_alignment": "string (left | center | split)"
    }}
  ]
}}
"""


# ==========================================
# STAGE 4: COMPONENT DETAILS
# ==========================================

COMPONENT_GENERATION = """Create a high-fidelity visual render of a specific premium UI Component.
Component Type: {component_type}
Visual Style & Specs:
- Theme: {visual_style_description}
- Brand Colors: Background {bg_color}, Accent {accent_color}, Muted {muted_color}
- Typographic suggestions: {header_font} for headers, {body_font} for body.

The component MUST be fully designed and rendered showing:
1. The default resting state of the component with perfect pixel-level spacing and layout alignment.
2. Hover state variations (e.g. card scaling, glow overlays, shifted vectors) shown side-by-side or as highlighted overlay annotations.
3. Exact typographic treatment, padding, borders, shadows, and subtle micro-details that make this element feel exceptionally premium.

Style: Highly detailed modern web UI component render, glassmorphism/skeuomorphism as appropriate, dark premium background.
Resolution: Pristine, incredibly sharp, vector-quality borders, beautiful gradients, 4k detail. NO generic placeholder content.
"""

COMPONENT_ANALYSIS = """You are an expert Design Systems Engineer AI. Analyze this high-fidelity UI component render and extract its visual specifications, structure, and spacing tokens as a structured JSON object matching the schema below.

Output ONLY valid JSON, starting with {{ and ending with }}, containing no explanations or markdown blocks.

JSON Schema:
{{
  "component_id": "string (e.g., 'hero_main', 'feature_bento', 'interactive_cta')",
  "name": "string (human-readable name, e.g. 'Luxury Bento Grid Component')",
  "visual_style": {{
    "layout": "string (e.g., 'flex-row', 'flex-col', 'grid-cols-3', 'asymmetric_split')",
    "background_treatment": "string (e.g. 'glassmorphism with backdrop-blur', 'flat high-contrast dark', 'vibrant radial gradient border')",
    "border_style": "string (e.g. '1px solid border-accent/20 with rounded corners')",
    "padding": "string (e.g., '2rem' or '3rem 2rem')",
    "gap": "string (e.g., '1rem' or '1.5rem')"
  }},
  "states": {{
    "default": "string (detailed visual look of default state)",
    "hover": "string (exact hover state transitions, scaling, color shifts, or glows)",
    "active": "string (active click/tap state look)"
  }},
  "interactivity": {{
    "cursor_type": "string (e.g. 'pointer', 'custom-magnetic')",
    "transition_duration": "string (e.g. '300ms')",
    "micro_interactions": ["string (e.g. 'scale on hover', 'accent glow sweep', 'text shift')"]
  }}
}}
"""


# ==========================================
# STAGE 5: MOTION STORYBOARD
# ==========================================

MOTION_STORYBOARD_GENERATION = """Create an exceptional UI Motion Design Storyboard showcasing the interactive scrolling reveal and transition animations.
Brand Concept: {brand_concept}
Visual Language:
- Aesthetic: {primary_emotion}
- Core Color Accent: {accent_color}
- Page Sections: {sections_list}

The storyboard MUST show a high-fidelity sequence containing:
1. 3 to 4 sequential keyframe panels presented side-by-side (Frame 1, Frame 2, Frame 3, Frame 4) detailing a scroll reveal or component transition.
2. Motion annotations, movement vectors, and directional arrows indicating elements entering, scaling, rotating, or fading.
3. An annotated cubic-bezier easing curve graph on the side showing the exact acceleration and deceleration timing profile.
4. Descriptions of interaction physics (e.g., spring physics, momentum damping, parallax depth layers).

Style: Technical UI/UX motion blueprint, side-by-side storyboard grid, technical storyboard symbols, dark sleek mode.
Resolution: Sharp details, clear frame divisions, legible labels, 4k quality.
"""

MOTION_STORYBOARD_ANALYSIS = """You are an expert Motion Director and UI Animator AI. Analyze this motion storyboard image and extract its precise keyframes, transition timing, physical parameters, and curves as a structured JSON object matching the schema below.
Interpret the frame sequence, directional arrows, easing graphs, and annotations to formulate a valid motion blueprint.

Output ONLY valid JSON, starting with {{ and ending with }}, containing no explanations or markdown blocks.

JSON Schema:
{{
  "animation_type": "string (e.g., 'scroll_reveal_stagger', 'parallax_slide_fade', 'bento_expand_3d')",
  "initial_state": {{
    "opacity": "number (0-1)",
    "transform": "string (e.g., 'translateY(80px) scale(0.9) rotate(-1deg)')"
  }},
  "final_state": {{
    "opacity": "number (0-1)",
    "transform": "string (e.g., 'translateY(0px) scale(1) rotate(0deg)')"
  }},
  "easing_curve": "string (e.g. 'cubic-bezier(0.16, 1, 0.3, 1)', 'cubic-bezier(0.25, 1, 0.5, 1)', 'spring(1, 80, 10, 0)')",
  "duration": "string (e.g. '0.8s' or '1.2s')",
  "pacing_feel": "string (e.g. 'cinematic', 'snappy-elastic', 'liquid-smooth', 'minimalist-sharp')",
  "scroll_trigger": {{
    "enabled": "boolean",
    "start_trigger": "string (e.g., 'top 80%')",
    "scrub": "boolean | number",
    "pin": "boolean"
  }},
  "stagger": {{
    "enabled": "boolean",
    "amount": "string (e.g. '0.1s')"
  }}
}}
"""
