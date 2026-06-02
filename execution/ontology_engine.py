import os
import json
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"

def load_json(relative_path: Path) -> list | dict:
    """Helper to load a JSON file from the data directory."""
    if not relative_path.exists():
        raise FileNotFoundError(f"Required ontology data file not found at: {relative_path}")
    return json.loads(relative_path.read_text(encoding="utf-8"))

def resolve_design_dna(dna: dict) -> dict:
    """
    Enriches a simple Design DNA dictionary with full, concrete design tokens 
    resolved from the ontology. Validates against the design graph rules.
    """
    # 1. Load ontology databases
    emotions = load_json(DATA_DIR / "ontology" / "emotions.json")
    archetypes = load_json(DATA_DIR / "ontology" / "brand_archetypes.json")
    motion_styles = load_json(DATA_DIR / "ontology" / "motion_styles.json")
    spatial_modes = load_json(DATA_DIR / "ontology" / "spatial_modes.json")
    colors_db = load_json(DATA_DIR / "ontology" / "color_psychology.json")
    typos_db = load_json(DATA_DIR / "ontology" / "typography_styles.json")
    interactions = load_json(DATA_DIR / "ontology" / "interaction_models.json")
    
    # 2. Extract input values
    core_emotion = dna.get("core_emotion", "trustworthy").lower()
    brand_arc = dna.get("brand_archetype", "everyman").lower()
    
    # 3. Find emotion profile matching input core_emotion
    emotion_profile = next((e for e in emotions if e["id"] == core_emotion), None)
    if not emotion_profile:
        # Fallback to trustworthy
        print(f"[WARN] Core emotion '{core_emotion}' not found in ontology. Falling back to 'trustworthy'.")
        emotion_profile = next(e for e in emotions if e["id"] == "trustworthy")
        core_emotion = "trustworthy"
        
    # Find brand archetype matching input brand_archetype
    archetype_profile = next((a for a in archetypes if a["id"] == brand_arc), None)
    if not archetype_profile:
        print(f"[WARN] Brand archetype '{brand_arc}' not found in ontology. Falling back to 'everyman'.")
        archetype_profile = next(a for a in archetypes if a["id"] == "everyman")
        brand_arc = "everyman"

    # 4. Resolve Concrete Properties using Emotion Profile references
    # Spatial Mode resolution
    # Fallback to the first available in profile or 'airy'/'dense'/'grid-heavy' depending on density
    density_val = dna.get("visual_density", emotion_profile.get("visual_density", "medium"))
    spatial_id = "grid-heavy"
    if core_emotion in ["luxury", "calm"]:
        spatial_id = "airy"
    elif core_emotion in ["cyberpunk", "aggressive"]:
        spatial_id = "dense"
    elif core_emotion == "playful":
        spatial_id = "modular"
    elif core_emotion == "editorial":
        spatial_id = "asymmetric"
        
    spatial_mode = next((s for s in spatial_modes if s["id"] == spatial_id), spatial_modes[0])

    # Color Palette resolution
    pref_colors = emotion_profile.get("preferred_colors", [])
    color_palette = None
    for pc in pref_colors:
        color_palette = next((c for c in colors_db if c["id"] == pc), None)
        if color_palette:
            break
    if not color_palette:
        # Try finding a palette that list this emotion
        color_palette = next((c for c in colors_db if core_emotion in c.get("emotions", [])), colors_db[0])
        
    # Typography Style resolution
    pref_typos = emotion_profile.get("preferred_typography", [])
    typo_style = None
    for pt in pref_typos:
        typo_style = next((t for t in typos_db if t["id"] == pt), None)
        if typo_style:
            break
    if not typo_style:
        typo_style = next((t for t in typos_db if core_emotion in t.get("emotions", [])), typos_db[0])
 
    # Motion Style resolution
    pref_motion_list = emotion_profile.get("preferred_motion", [])
    motion_style = None
    for pm in pref_motion_list:
        motion_style = next((m for m in motion_styles if m["id"] == pm), None)
        if motion_style:
            break
    if not motion_style:
        motion_style = next((m for m in motion_styles if m["id"] == "minimal"), motion_styles[0])

    # Interaction Model resolution
    interaction_id = "minimal"
    if core_emotion in ["luxury", "avant-garde", "mysterious"]:
        interaction_id = "immersive"
    elif core_emotion in ["cyberpunk", "aggressive", "energetic"]:
        interaction_id = "reactive"
    elif core_emotion == "playful":
        interaction_id = "gesture-driven"
        
    interaction_model = next((i for i in interactions if i["id"] == interaction_id), interactions[0])

    # 5. Load and select best pattern from patterns library
    patterns = load_json(DATA_DIR / "patterns" / "hero_patterns.json")
    # Score patterns based on best_for list and emotion score match
    scored_patterns = []
    for pat in patterns:
        score = 0
        if core_emotion in pat.get("best_for", []):
            score += 5
        if brand_arc in pat.get("best_for", []):
            score += 3
        # Match against emotion_scores
        score += pat.get("emotion_scores", {}).get(core_emotion, 0)
        scored_patterns.append((score, pat))
    
    # Sort and take the best
    scored_patterns.sort(key=lambda x: x[0], reverse=True)
    best_pattern = scored_patterns[0][1] if scored_patterns else None

    # Assemble enriched tokens
    enriched_tokens = {
        "metadata": {
            "version": "1.0",
            "session_prompt": dna.get("prompt_hint", ""),
            "applied_warnings": [],
            "applied_corrections": []
        },
        "brand": {
            "archetype": archetype_profile["id"],
            "name": archetype_profile["name"],
            "description": archetype_profile["description"]
        },
        "emotion": {
            "id": emotion_profile["id"],
            "name": emotion_profile["name"],
            "visual_density": density_val,
            "motion_energy": dna.get("motion_energy", emotion_profile.get("energy", 5))
        },
        "colors": {
            "palette_id": color_palette["id"],
            "palette_name": color_palette["name"],
            "background": color_palette["background"],
            "foreground": color_palette["foreground"],
            "accent": color_palette["accent"],
            "muted": color_palette["muted"]
        },
        "typography": {
            "style_id": typo_style["id"],
            "style_name": typo_style["name"],
            "header_font": typo_style["header_font"],
            "body_font": typo_style["body_font"],
            "header_weight": typo_style["header_weight"],
            "body_weight": typo_style["body_weight"],
            "letter_spacing": typo_style["letter_spacing"]
        },
        "spatial": {
            "mode_id": spatial_mode["id"],
            "mode_name": spatial_mode["name"],
            "padding_y": spatial_mode["layout_rules"]["section_padding_y"],
            "container_width": spatial_mode["layout_rules"]["container_max_width"],
            "grid_gap": spatial_mode["layout_rules"]["grid_gap"],
            "asymmetrical": spatial_mode["layout_rules"]["asymmetrical"],
            "borders_visible": spatial_mode["layout_rules"]["border_visible"]
        },
        "motion": {
            "style_id": motion_style["id"],
            "style_name": motion_style["name"],
            "type": motion_style["type"],
            "config": motion_style["config"]
        },
        "interaction": {
            "model_id": interaction_model["id"],
            "cursor": interaction_model["cursor_type"],
            "hover": interaction_model["hover_effect"],
            "scroll": interaction_model["scroll_control"],
            "active": interaction_model["active_state"]
        },
        "selected_pattern": best_pattern
    }

    # 6. Apply design rules validation from design_rules.json
    rules = load_json(DATA_DIR / "graph" / "design_rules.json")
    for rule in rules.get("compatibility_rules", []):
        source_type = rule["source_type"]
        source_val = rule["source_val"]
        target_type = rule["target_type"]
        constraint = rule["constraint"]
        values = rule["values"]
        severity = rule["severity"]
        msg = rule["message"]
        
        # Check if source triggers
        triggered = False
        if source_type == "emotion" and enriched_tokens["emotion"]["id"] == source_val:
            triggered = True
            
        if triggered:
            # Check target property against constraint
            violates = False
            
            # Fetch target property value
            target_val = None
            if target_type == "visual_density":
                target_val = enriched_tokens["emotion"]["visual_density"]
            elif target_type == "motion_energy":
                target_val = enriched_tokens["emotion"]["motion_energy"]
            elif target_type == "color_psychology":
                target_val = enriched_tokens["colors"]["palette_id"]
            elif target_type == "typography_styles":
                target_val = enriched_tokens["typography"]["style_id"]
            elif target_type == "motion_styles":
                target_val = enriched_tokens["motion"]["style_id"]
                
            # Perform check
            if constraint == "equals":
                violates = (target_val not in values)
            elif constraint == "less_than_or_equal":
                violates = (target_val > values[0])
            elif constraint == "in":
                violates = (target_val not in values)
            elif constraint == "not_in":
                violates = (target_val in values)
                
            if violates:
                log_entry = {
                    "rule_id": rule["rule_id"],
                    "message": msg
                }
                if severity == "error":
                    # Rectify: Apply the required values automatically to comply
                    enriched_tokens["metadata"]["applied_corrections"].append(log_entry)
                    print(f"[ONTOLOGY ERROR CORRECTION] {msg}")
                    # Apply correction
                    if target_type == "visual_density":
                        enriched_tokens["emotion"]["visual_density"] = values[0]
                    elif target_type == "motion_energy":
                        enriched_tokens["emotion"]["motion_energy"] = values[0]
                    elif target_type == "color_psychology":
                        new_palette = next((c for c in colors_db if c["id"] == values[0]), colors_db[0])
                        enriched_tokens["colors"] = {
                            "palette_id": new_palette["id"],
                            "palette_name": new_palette["name"],
                            "background": new_palette["background"],
                            "foreground": new_palette["foreground"],
                            "accent": new_palette["accent"],
                            "muted": new_palette["muted"]
                        }
                    elif target_type == "typography_styles":
                        new_typo = next((t for t in typos_db if t["id"] == values[0]), typos_db[0])
                        enriched_tokens["typography"] = {
                            "style_id": new_typo["id"],
                            "style_name": new_typo["name"],
                            "header_font": new_typo["header_font"],
                            "body_font": new_typo["body_font"],
                            "header_weight": new_typo["header_weight"],
                            "body_weight": new_typo["body_weight"],
                            "letter_spacing": new_typo["letter_spacing"]
                        }
                else:
                    enriched_tokens["metadata"]["applied_warnings"].append(log_entry)
                    print(f"[ONTOLOGY WARNING] {msg}")

    return enriched_tokens

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        dna_input = json.loads(sys.argv[1])
        print(json.dumps(resolve_design_dna(dna_input), indent=2, ensure_ascii=False))
    else:
        # Dry run with mock data
        mock_dna = {
            "brand_archetype": "ruler",
            "core_emotion": "luxury",
            "visual_density": "high",  # This violates the luxury low-density rule! Should trigger correction.
            "motion_energy": 6,
            "primary_colors": ["matte-black", "gold"],
            "target_audience": "high-net-worth",
            "keywords": ["exclusive", "elite"],
            "prompt_hint": "A luxury boutique hotel branding"
        }
        print("Dry running with mock luxury DNA (violating density rule):")
        resolved = resolve_design_dna(mock_dna)
        print(json.dumps(resolved, indent=2, ensure_ascii=False))
