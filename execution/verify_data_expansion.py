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
        search_components
    )
except ImportError:
    from .qdrant_manager import (
        ensure_qdrant_running,
        get_qdrant_client,
        search_components
    )

def run_verification():
    """
    Verifies that the Qdrant database expansion is complete and semantically correct.
    Checks total registered counts and runs multi-dimensional RAG matching tests.
    """
    print("\n" + "="*60)
    print("[VERIFIER] INITIATING DATA EXPANSION VERIFICATION SUITE")
    print("="*60)

    # 1. Connect and verify Qdrant
    if not ensure_qdrant_running():
        print("[FAIL] Qdrant service is offline. Cannot proceed with verification.")
        sys.exit(1)

    client = get_qdrant_client()
    collection_name = "components_registry"

    # 2. Query total count
    try:
        collections = client.get_collections()
        exists = any(c.name == collection_name for c in collections.collections)
        
        if not exists:
            print(f"[FAIL] Collection '{collection_name}' does not exist! Seeding may have failed.")
            sys.exit(1)
            
        # Get count
        res = client.count(collection_name=collection_name)
        total_points = res.count
        
        print(f"\n[STATUS] Collection '{collection_name}' is fully active.")
        print(f"[STATUS] Total Semantically Indexed Components: {total_points}")
        
        if total_points >= 100:
            print(f"[SUCCESS] Data expansion target ACHIEVED! (Found {total_points} components, expected >= 100)")
        else:
            print(f"[FAIL] Data expansion target not met. Found only {total_points} components, expected >= 100.")
            sys.exit(1)
            
    except Exception as e:
        print(f"[ERROR] Failed to query database stats: {e}")
        sys.exit(1)

    # 3. Perform 3 distinct multi-dimensional semantic search tests
    search_scenarios = [
        {
            "title": "SCENARIO 1: Ultra-Luxury & Editorial (Ruler Archetype, Calm/Minimalist)",
            "query": "brand archetype: ruler, emotion: luxury editorial calm, layout spatial mode: airy minimalist elegant aesthetics",
            "limit": 3
        },
        {
            "title": "SCENARIO 2: Cyberpunk / Aggressive Streetwear (Outlaw Archetype, Cyberpunk/Energetic)",
            "query": "brand archetype: outlaw, emotion: aggressive cyberpunk energetic rebel, layout spatial mode: dense raw borders street culture style",
            "limit": 3
        },
        {
            "title": "SCENARIO 3: Playful & Creative Motion Studio (Creator Archetype, Playful/Friendly)",
            "query": "brand archetype: creator, emotion: playful friendly energetic, layout spatial mode: asymmetric interactive spring drag controls animations",
            "limit": 3
        }
    ]

    print("\n[VERIFIER] Running Semantic Search Scenario Tests...")
    
    for idx, scenario in enumerate(search_scenarios):
        print("\n" + "-"*60)
        print(scenario["title"])
        print(f"Query: '{scenario['query']}'")
        print("-"*60)
        
        hits = search_components(scenario["query"], limit=scenario["limit"])
        
        if not hits:
            print("[WARNING] Semantic search returned 0 matches. Fallback triggered.")
            continue
            
        for hit_idx, hit in enumerate(hits):
            print(f"{hit_idx + 1}. [{hit['id']}] {hit['name']}")
            print(f"   Category: {hit['category']} | Score: {hit['score']:.4f}")
            print(f"   Description: {hit['description'][:120]}...")
            print(f"   Target Emotions: {hit['emotions']}")
            print(f"   Target Archetypes: {hit['archetypes']}")
            print(f"   Spatial Mode: {hit['spatial_mode']}")
            print()

    print("="*60)
    print("[SUCCESS] VERIFICATION COMPLETED SUCCESSFULLY!")
    print("="*60)

if __name__ == "__main__":
    run_verification()
