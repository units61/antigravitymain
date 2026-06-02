import os
import json
import shutil
import subprocess
import sys
from pathlib import Path

try:
    from execution.theme_generator import generate_theme
except ImportError:
    # Fallback for when the script is run directly from the execution folder
    from theme_generator import generate_theme

try:
    from execution.ai_compiler import compile_component_from_scratch
except ImportError:
    try:
        from ai_compiler import compile_component_from_scratch
    except ImportError:
        compile_component_from_scratch = None


# Setup base paths
EXECUTION_DIR = Path(__file__).parent
BASE_DIR = EXECUTION_DIR.parent
TEMPLATES_DIR = EXECUTION_DIR / "templates"
TMP_DIR = BASE_DIR / ".tmp"
BUILDS_DIR = TMP_DIR / "builds"

def serialize_value_to_js(val) -> str:
    """Serializes Python values to JS literal representations (JSON format works for objects/lists)."""
    return json.dumps(val, indent=2, ensure_ascii=False)

def assemble_next_app(blueprint_path: Path, session_id: str = None) -> Path:
    """
    Reads the Experience Blueprint JSON and compiles a fully resolved
    Next.js + TailwindCSS application inside .tmp/builds/{session_id}/
    """
    print(f"\n==================================================")
    print(f"[ASSEMBLER] STARTING NEXT.JS APP ASSEMBLY")
    print(f"Blueprint: {blueprint_path}")
    
    # 1. Load blueprint data
    if not blueprint_path.exists():
        raise FileNotFoundError(f"Experience blueprint not found at {blueprint_path}")
        
    blueprint = json.loads(blueprint_path.read_text(encoding="utf-8"))
    
    if not session_id:
        session_id = blueprint.get("metadata", {}).get("session_id", "dynamic_session")
        
    target_dir = BUILDS_DIR / session_id
    print(f"Target Build Dir: {target_dir}")
    print(f"==================================================\n")
    
    # 2. Re-create base directory structure safely
    if target_dir.exists():
        print(f"[ASSEMBLER] Target directory exists. Safely clearing generated subfolders without deleting parent dir...")
        # Safe clear of specific folders instead of whole folder rmtree (to avoid WinError 32 locked files)
        for folder_name in ["app", "components", "hooks"]:
            sub_dir = target_dir / folder_name
            if sub_dir.exists():
                for item in sub_dir.iterdir():
                    if item.is_file():
                        try:
                            item.unlink()
                        except Exception as e:
                            print(f"[WARNING] Could not delete file {item}: {e}")
        
    # Directories
    app_dir = target_dir / "app"
    components_dir = target_dir / "components"
    hooks_dir = target_dir / "hooks"
    app_dir.mkdir(parents=True, exist_ok=True)
    components_dir.mkdir(parents=True, exist_ok=True)
    hooks_dir.mkdir(parents=True, exist_ok=True)
    
    # 2b. Isolated Node Modules Strategy: Instead of Directory Junction (which causes Next.js/React context-split hydration bugs),
    # we let npm install handle it cleanly in the local directory.
    pass
    
    # 3. Copy configuration files from templates
    print(f"[ASSEMBLER] Copying Next.js configuration files...")
    shutil.copy(TEMPLATES_DIR / "package.json.template", target_dir / "package.json")
    shutil.copy(TEMPLATES_DIR / "tailwind.config.js.template", target_dir / "tailwind.config.js")
    shutil.copy(TEMPLATES_DIR / "postcss.config.js.template", target_dir / "postcss.config.js")
    shutil.copy(TEMPLATES_DIR / "app" / "layout.js.template", app_dir / "layout.js")
    
    # 3b. Copy hooks
    src_hooks_dir = TEMPLATES_DIR / "hooks"
    if src_hooks_dir.exists():
        print(f"[ASSEMBLER] Copying custom react hooks...")
        for hook_file in src_hooks_dir.glob("*.js"):
            shutil.copy(hook_file, hooks_dir / hook_file.name)
            
    # 3c. Copy helper components (used globally or inside other components)
    for helper in ["SmoothScroll.jsx", "MagneticButton.jsx", "GlowCard.jsx"]:
        helper_src = TEMPLATES_DIR / "components" / helper
        if helper_src.exists():
            print(f"[ASSEMBLER] Copying helper component: {helper}...")
            shutil.copy(helper_src, components_dir / helper)
    
    # 4. Generate dynamic theme stylesheet globals.css
    visual_lang = blueprint.get("visual_language", {})
    generate_theme(visual_lang, app_dir / "globals.css")
    
    # 4b. Check if dynamic 3D Scene State exists in session directory
    scene_state_path = blueprint_path.parent / "scene_state.json"
    is_3d_experience = scene_state_path.exists()
    
    if is_3d_experience:
        print("[ASSEMBLER] Detected 3D WebGL Experience! Integrating UniversalScene...")
        shutil.copy(TEMPLATES_DIR / "components" / "UniversalScene.jsx", components_dir / "UniversalScene.jsx")

    # 5. Copy mapped components into components directory
    component_plan = blueprint.get("component_plan", {})
    mapped_components = component_plan.get("mapped_components", [])
    
    print(f"[ASSEMBLER] Copying component registry JSX files...")
    used_components = set()
    
    for mapped in mapped_components:
        comp_id = mapped.get("component_id")
        if comp_id == "SplitSection":
            comp_id = "SplitSectionHero"
            
        # RAG Dynamic Seeding Check
        is_dynamic_rag = mapped.get("is_dynamic_rag", False)
        jsx_code = mapped.get("jsx_code", "")
        if is_dynamic_rag and jsx_code:
            print(f"[ASSEMBLER] Seeding dynamic RAG component '{comp_id}' from Qdrant vector payload...")
            dest_comp = components_dir / f"{comp_id}.jsx"
            dest_comp.write_text(jsx_code, encoding="utf-8")
            used_components.add(comp_id)
            continue
            
        # Dynamic AI Compiler (Sonsuz Olasılık Motoru - Phase 1)
        compiled_jsx = ""
        if compile_component_from_scratch and os.getenv("OPENROUTER_API_KEY"):
            try:
                compiled_jsx = compile_component_from_scratch(
                    comp_id,
                    mapped,
                    blueprint.get("visual_language", {}),
                    blueprint.get("design_dna", {}),
                    blueprint.get("motion_graph", {}),
                    vision_ref=mapped.get("vision_reference_path", None)
                )
                
                # Strict Validation: Fallback if model refused or outputted invalid code stubs
                if compiled_jsx and ("I'm sorry" in compiled_jsx or "can't assist" in compiled_jsx or "export default" not in compiled_jsx):
                    print(f"[ASSEMBLER WARNING] AI Compiler returned safety refusal or invalid stub for '{comp_id}'. Triggering template fallback.")
                    compiled_jsx = ""
            except Exception as e:
                print(f"[ASSEMBLER WARNING] Scratch AI Compiler failed: {e}. Falling back to templates.")
                
        if compiled_jsx:
            print(f"[ASSEMBLER] Custom AI component '{comp_id}' compiled from scratch!")
            dest_comp = components_dir / f"{comp_id}.jsx"
            dest_comp.write_text(compiled_jsx, encoding="utf-8")
            used_components.add(comp_id)
            continue
            
        # Safety fallback check for catalog component ids
        src_comp = TEMPLATES_DIR / "components" / f"{comp_id}.jsx"
        if not src_comp.exists():
            print(f"[WARNING] Component {comp_id} not found in template registry. Finding fallback...")
            lower_id = comp_id.lower()
            if "hero" in lower_id:
                comp_id = "ImmersiveHero"
            elif "split" in lower_id:
                comp_id = "SplitSectionHero"
            elif "bento" in lower_id:
                comp_id = "BentoGrid"
            elif "marquee" in lower_id:
                comp_id = "Marquee"
            elif "parallax" in lower_id:
                comp_id = "ParallaxGallery"
            elif "magnetic" in lower_id:
                comp_id = "MagneticButton"
            elif "reveal" in lower_id:
                comp_id = "TextReveal"
            elif "testimonial" in lower_id:
                comp_id = "TestimonialCarousel"
            elif "counter" in lower_id or "stats" in lower_id:
                comp_id = "StatsCounter"
            elif "pin" in lower_id:
                comp_id = "ScrollPinSection"
            elif "cta" in lower_id:
                comp_id = "MotionCTA"
            elif "footer" in lower_id:
                comp_id = "GlassmorphicFooter"
            elif "gallery" in lower_id:
                comp_id = "InteractiveGallery"
            else:
                comp_id = "FeatureGrid"
            src_comp = TEMPLATES_DIR / "components" / f"{comp_id}.jsx"
            
        shutil.copy(src_comp, components_dir / f"{comp_id}.jsx")
        used_components.add(comp_id)
        
    print(f"[ASSEMBLER] Extracted {len(used_components)} registry components for page layout: {used_components}")
    
    # 6. Generate dynamic app/page.js with imports and serialized props injection
    print(f"[ASSEMBLER] Compiling dynamic React App page...")
    
    if is_3d_experience:
        scene_state_data = json.loads(scene_state_path.read_text(encoding="utf-8"))
        js_scene_state = serialize_value_to_js(scene_state_data)
        
        imports_block = f"""\"use client\";

import React from "react";
import dynamic from "next/dynamic";

const UniversalScene = dynamic(() => import("../components/UniversalScene"), {{
  ssr: false,
  loading: () => (
    <div className="w-full h-screen bg-[#FFF7F2] flex items-center justify-center text-[#ffa27c] font-mono text-[10px] tracking-[0.2em] uppercase">
      Loading 3D Studio...
    </div>
  )
}});
"""
        for comp in used_components:
            imports_block += f'import {comp} from "../components/{comp}";\n'
            
        render_block = f"""
export default function Home() {{
  const sceneState = {js_scene_state};

  return (
    <main className="relative w-full min-h-screen bg-[#FFF7F2] overflow-x-hidden">
      <style>{{`
        section, footer {{
          background-color: transparent !important;
        }}
      `}}</style>
      
      {{/* Background WebGL canvas */}}
      <div className="fixed inset-0 z-0 pointer-events-none">
        <UniversalScene sceneState={{sceneState}} />
      </div>
      
      {{/* Foreground 2D HTML Layout */}}
      <div className="relative z-10 w-full h-auto">
"""
        for i, mapped in enumerate(mapped_components):
            comp_id = mapped.get("component_id")
            if comp_id == "SplitSection":
                comp_id = "SplitSectionHero"
                
            # Fallback check again
            if comp_id not in used_components:
                # Match fallback used
                lower_id = comp_id.lower()
                if "hero" in lower_id:
                    comp_id = "ImmersiveHero"
                elif "split" in lower_id:
                    comp_id = "SplitSectionHero"
                elif "bento" in lower_id:
                    comp_id = "BentoGrid"
                elif "marquee" in lower_id:
                    comp_id = "Marquee"
                elif "parallax" in lower_id:
                    comp_id = "ParallaxGallery"
                elif "magnetic" in lower_id:
                    comp_id = "MagneticButton"
                elif "reveal" in lower_id:
                    comp_id = "TextReveal"
                elif "testimonial" in lower_id:
                    comp_id = "TestimonialCarousel"
                elif "counter" in lower_id or "stats" in lower_id:
                    comp_id = "StatsCounter"
                elif "pin" in lower_id:
                    comp_id = "ScrollPinSection"
                elif "cta" in lower_id:
                    comp_id = "MotionCTA"
                elif "footer" in lower_id:
                    comp_id = "GlassmorphicFooter"
                elif "gallery" in lower_id:
                    comp_id = "InteractiveGallery"
                else:
                    comp_id = "FeatureGrid"
                    
            resolved_props = mapped.get("resolved_props", {})
            motion_config = mapped.get("motion_config", {})
            
            # Serialize specific fields
            title = resolved_props.get("title", "")
            subtitle = resolved_props.get("subtitle", "")
            eyebrow = resolved_props.get("eyebrow", "")
            colors = resolved_props.get("colors", {})
            items = resolved_props.get("items", [])
            primary_cta = resolved_props.get("primary_cta", {})
            
            # Format inline variables for properties serialization inside component
            js_title = serialize_value_to_js(title)
            js_subtitle = serialize_value_to_js(subtitle)
            js_eyebrow = serialize_value_to_js(eyebrow)
            js_colors = serialize_value_to_js(colors)
            js_items = serialize_value_to_js(items)
            js_cta = serialize_value_to_js(primary_cta)
            js_motion = serialize_value_to_js(motion_config)
            
            render_block += f"        <{comp_id}\n"
            render_block += f"          title={js_title}\n"
            render_block += f"          subtitle={js_subtitle}\n"
            if eyebrow:
                render_block += f"          eyebrow={js_eyebrow}\n"
            if colors:
                render_block += f"          colors={{{js_colors}}}\n"
            if items:
                render_block += f"          items={{{js_items}}}\n"
            if primary_cta:
                render_block += f"          primary_cta={{{js_cta}}}\n"
            render_block += f"          motion_config={{{js_motion}}}\n"
            render_block += f"        />\n\n"
            
        render_block += """      </div>
    </main>
  );
}
"""
        page_content = f"{imports_block}\n{render_block}"
        (app_dir / "page.js").write_text(page_content, encoding="utf-8")
    else:
        imports_block = '"use client";\n\nimport React from "react";\n'
        for comp in used_components:
            imports_block += f'import {comp} from "../components/{comp}";\n'
            
        render_block = 'export default function Home() {\n  return (\n    <main className="relative w-full min-h-screen flex flex-col bg-background overflow-hidden">\n'
        
        for i, mapped in enumerate(mapped_components):
            comp_id = mapped.get("component_id")
            if comp_id == "SplitSection":
                comp_id = "SplitSectionHero"
                
            # Fallback check again
            if comp_id not in used_components:
                # Match fallback used
                lower_id = comp_id.lower()
                if "hero" in lower_id:
                    comp_id = "ImmersiveHero"
                elif "split" in lower_id:
                    comp_id = "SplitSectionHero"
                elif "bento" in lower_id:
                    comp_id = "BentoGrid"
                elif "marquee" in lower_id:
                    comp_id = "Marquee"
                elif "parallax" in lower_id:
                    comp_id = "ParallaxGallery"
                elif "magnetic" in lower_id:
                    comp_id = "MagneticButton"
                elif "reveal" in lower_id:
                    comp_id = "TextReveal"
                elif "testimonial" in lower_id:
                    comp_id = "TestimonialCarousel"
                elif "counter" in lower_id or "stats" in lower_id:
                    comp_id = "StatsCounter"
                elif "pin" in lower_id:
                    comp_id = "ScrollPinSection"
                elif "cta" in lower_id:
                    comp_id = "MotionCTA"
                elif "footer" in lower_id:
                    comp_id = "GlassmorphicFooter"
                elif "gallery" in lower_id:
                    comp_id = "InteractiveGallery"
                else:
                    comp_id = "FeatureGrid"
                    
            resolved_props = mapped.get("resolved_props", {})
            motion_config = mapped.get("motion_config", {})
            
            # Serialize specific fields
            title = resolved_props.get("title", "")
            subtitle = resolved_props.get("subtitle", "")
            eyebrow = resolved_props.get("eyebrow", "")
            colors = resolved_props.get("colors", {})
            items = resolved_props.get("items", [])
            primary_cta = resolved_props.get("primary_cta", {})
            
            # Format inline variables for properties serialization inside component
            js_title = serialize_value_to_js(title)
            js_subtitle = serialize_value_to_js(subtitle)
            js_eyebrow = serialize_value_to_js(eyebrow)
            js_colors = serialize_value_to_js(colors)
            js_items = serialize_value_to_js(items)
            js_cta = serialize_value_to_js(primary_cta)
            js_motion = serialize_value_to_js(motion_config)
            
            render_block += f"      <{comp_id}\n"
            render_block += f"        title={js_title}\n"
            render_block += f"        subtitle={js_subtitle}\n"
            if eyebrow:
                render_block += f"        eyebrow={js_eyebrow}\n"
            if colors:
                render_block += f"        colors={{{js_colors}}}\n"
            if items:
                render_block += f"        items={{{js_items}}}\n"
            if primary_cta:
                render_block += f"        primary_cta={{{js_cta}}}\n"
            render_block += f"        motion_config={{{js_motion}}}\n"
            render_block += f"      />\n\n"
            
        render_block += "    </main>\n  );\n}\n"
        
        page_content = f"{imports_block}\n{render_block}"
        (app_dir / "page.js").write_text(page_content, encoding="utf-8")
    
    print(f"\n[SUCCESS] ASSEMBLY COMPLETED!")
    print(f"Generated Next.js application written to: {target_dir}")
    print(f"==================================================\n")
    
    return target_dir

if __name__ == "__main__":
    # Test assembly using cached test run blueprint
    test_run_blueprint = BASE_DIR / ".tmp" / "pipeline" / "test_run_1" / "experience_blueprint.json"
    if test_run_blueprint.exists():
        assemble_next_app(test_run_blueprint, "test_run_next_app")
    else:
        print("[WARNING] Could not find test run blueprint. Please execute test_pipeline.py first to create a blueprint.")
