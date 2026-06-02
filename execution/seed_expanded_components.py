import os
import sys
from pathlib import Path

# Setup path so execution imports work cleanly
EXECUTION_DIR = Path(__file__).parent
sys.path.append(str(EXECUTION_DIR))

try:
    from qdrant_manager import (
        ensure_qdrant_running,
        get_qdrant_client,
        get_embedding_model,
        COMPONENT_METADATA_REGISTRY,
        TEMPLATES_DIR
    )
    from expanded_components_db import EXPANDED_COMPONENTS
except ImportError:
    # Try alternate imports if run differently
    from .qdrant_manager import (
        ensure_qdrant_running,
        get_qdrant_client,
        get_embedding_model,
        COMPONENT_METADATA_REGISTRY,
        TEMPLATES_DIR
    )
    from .expanded_components_db import EXPANDED_COMPONENTS

def seed_database():
    """
    Populates Qdrant components_registry with the full set of 100+ premium UI components.
    Consolidates baseline physical templates and programmatic expanded database.
    """
    print("\n" + "="*60)
    print("[SEEDER] INITIATING DATASET EXPANSION (100+ PREMIUM COMPONENTS)")
    print("="*60)

    # 1. Ensure Qdrant is running
    if not ensure_qdrant_running():
        print("[ERROR] Docker or Qdrant port 6333 is not active. Seeding aborted.")
        return False

    client = get_qdrant_client()
    model = get_embedding_model()
    if not client or not model:
        print("[ERROR] Failed to load QdrantClient or FastEmbed. Seeding aborted.")
        return False

    collection_name = "components_registry"

    # 2. Re-create collection to ensure a clean state
    from qdrant_client.models import Distance, VectorParams
    try:
        collections = client.get_collections()
        exists = any(c.name == collection_name for c in collections.collections)
        if exists:
            print(f"[SEEDER] Recreating clean collection '{collection_name}'...")
            client.delete_collection(collection_name)
            
        client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=384, distance=Distance.COSINE),
        )
        print(f"[SEEDER] Clean collection '{collection_name}' created.")
    except Exception as e:
        print(f"[ERROR] Failed to manage collection: {e}")
        return False

    # 3. Read physical baseline templates (20 total)
    print("\n[SEEDER] Step 1: Processing physical template baseline components...")
    physical_components = []
    
    # Let's read files from TEMPLATES_DIR
    if TEMPLATES_DIR.exists():
        physical_files = list(TEMPLATES_DIR.glob("*.jsx"))
        print(f"[SEEDER] Found {len(physical_files)} physical templates in templates folder.")
        
        # We match these physical files with metadata from COMPONENT_METADATA_REGISTRY, or generate auto-metadata
        for idx, file_path in enumerate(physical_files):
            comp_id = file_path.stem
            jsx_code = file_path.read_text(encoding="utf-8")
            
            # Find in metadata registry or create auto-metadata
            meta = next((c for c in COMPONENT_METADATA_REGISTRY if c["id"] == comp_id), None)
            if not meta:
                # Fallback meta if file exists but not in the static 13 metadata registry
                category = "showcase"
                if "hero" in comp_id.lower():
                    category = "hero"
                elif "footer" in comp_id.lower():
                    category = "footer"
                elif "cta" in comp_id.lower():
                    category = "cta"
                elif "button" in comp_id.lower() or "scroll" in comp_id.lower():
                    category = "utility"
                elif "gallery" in comp_id.lower():
                    category = "gallery"
                elif "reveal" in comp_id.lower() or "text" in comp_id.lower():
                    category = "text"
                elif "carousel" in comp_id.lower() or "reviews" in comp_id.lower():
                    category = "reviews"
                
                meta = {
                    "id": comp_id,
                    "name": comp_id.replace("Asymmetric", "Asymmetric ").replace("Grid", " Grid").replace("Hero", " Hero"),
                    "category": category,
                    "description": f"Ultra-premium custom React component: {comp_id}. Highly optimized, modular, responsive layout with customized brand aesthetic configurations.",
                    "emotions": ["luxury", "calm", "editorial"],
                    "archetypes": ["creator", "ruler", "sage"],
                    "spatial_mode": "standard"
                }
                
            physical_components.append({
                "id": meta["id"],
                "name": meta["name"],
                "category": meta["category"],
                "description": meta["description"],
                "emotions": meta["emotions"],
                "archetypes": meta["archetypes"],
                "spatial_mode": meta["spatial_mode"],
                "jsx_code": jsx_code
            })
            
    print(f"[SEEDER] Compiled {len(physical_components)} baseline templates with full JSX codes.")

    # 4. Integrate expanded premium components from database (85 total)
    print("\n[SEEDER] Step 2: Integrating programmatic premium expanded components database...")
    print(f"[SEEDER] Loaded {len(EXPANDED_COMPONENTS)} components from expanded_components_db.py.")

    # 5. Consolidate and resolve duplicates
    total_components = []
    seen_ids = set()

    for comp in physical_components:
        if comp["id"] not in seen_ids:
            total_components.append(comp)
            seen_ids.add(comp["id"])

    for comp in EXPANDED_COMPONENTS:
        if comp["id"] not in seen_ids:
            total_components.append(comp)
            seen_ids.add(comp["id"])
        else:
            # If id clashes, append a suffix to keep both
            comp["id"] = f"{comp['id']}_Gen"
            comp["name"] = f"{comp['name']} (Gen)"
            total_components.append(comp)
            seen_ids.add(comp["id"])

    print(f"\n[SEEDER] Consolidating complete dataset... Total distinct components: {len(total_components)}")
    
    # 6. Generate Embeddings & Upsert to Qdrant
    print(f"\n[SEEDER] Step 3: Generating BGE vector embeddings for {len(total_components)} items...")
    
    documents = []
    ids = []
    payloads = []

    for idx, comp in enumerate(total_components):
        comp_id = comp["id"]
        # Format text representation for the vector model to index semantically
        embedding_text = f"Component ID: {comp_id}\n"
        embedding_text += f"Category: {comp['category']}\n"
        embedding_text += f"Name: {comp['name']}\n"
        embedding_text += f"Description: {comp['description']}\n"
        embedding_text += f"Target Emotions: {', '.join(comp['emotions'])}\n"
        embedding_text += f"Target Archetypes: {', '.join(comp['archetypes'])}\n"
        embedding_text += f"Spatial Layout Mode: {comp['spatial_mode']}"
        
        documents.append(embedding_text)
        ids.append(idx)
        payloads.append(comp)

    try:
        embeddings = list(model.embed(documents))
        
        # Upload using Qdrant Points structure
        from qdrant_client.models import PointStruct
        points = []
        for i, vector in enumerate(embeddings):
            vec_list = vector.tolist() if hasattr(vector, "tolist") else list(vector)
            points.append(PointStruct(
                id=ids[i],
                vector=vec_list,
                payload=payloads[i]
            ))
            
        # Segment uploads into batches to be safe and responsive
        batch_size = 50
        for b_idx in range(0, len(points), batch_size):
            batch = points[b_idx : b_idx + batch_size]
            client.upsert(collection_name=collection_name, points=batch)
            print(f"[SEEDER] Upserted batch {b_idx // batch_size + 1} ({len(batch)} points)...")
            
        print("\n" + "="*60)
        print(f"[SUCCESS] QDRANT SEEDING COMPLETE!")
        print(f"Total Components Registered: {len(total_components)}")
        print("FastEmbed Local Model: BAAI/bge-small-en-v1.5 (dimension 384)")
        print("="*60)
        return True
        
    except Exception as e:
        print(f"[ERROR] Failed to index vectors in Qdrant: {e}")
        return False

if __name__ == "__main__":
    seed_database()
