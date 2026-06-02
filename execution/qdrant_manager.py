import os
import sys
import time
import subprocess
import socket
from pathlib import Path
import json

# Setup base paths
EXECUTION_DIR = Path(__file__).parent
BASE_DIR = EXECUTION_DIR.parent
TEMPLATES_DIR = EXECUTION_DIR / "templates" / "components"

# Lazy load heavy ML/Database clients to keep import speed fast when RAG is disabled
_qdrant_client = None
_embedding_model = None

def is_docker_running() -> bool:
    """Checks if the local Docker daemon is running."""
    try:
        result = subprocess.run(["docker", "info"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=5)
        return result.returncode == 0
    except Exception:
        return False

def check_container_state(name: str) -> str:
    """Returns 'running', 'stopped', or 'missing' for a container name."""
    if not is_docker_running():
        return "missing"
    try:
        # Check running
        res = subprocess.run(["docker", "ps", "--filter", f"name={name}", "--format", "{{.Names}}"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if name in res.stdout:
            return "running"
        # Check all
        res_all = subprocess.run(["docker", "ps", "-a", "--filter", f"name={name}", "--format", "{{.Names}}"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if name in res_all.stdout:
            return "stopped"
        return "missing"
    except Exception:
        return "missing"

def ensure_qdrant_running() -> bool:
    """
    Ensures that a local Qdrant instance is running on port 6333.
    If not, attempts to start it via local Docker container 'andip-qdrant'.
    Returns True if successfully running, False otherwise.
    """
    # 1. First check if port 6333 is already responsive (maybe self-hosted without docker or already running)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(1)
        if s.connect_ex(("localhost", 6333)) == 0:
            print("[QDRANT] Qdrant port 6333 is open and active.")
            return True

    print("[QDRANT] Port 6333 is closed. Attempting to manage local Docker container...")

    # 2. Check if Docker is installed & running
    if not is_docker_running():
        print("[WARNING] Docker daemon is not running or not installed. Please launch Docker Desktop to enable local Qdrant.")
        return False

    state = check_container_state("andip-qdrant")
    print(f"[QDRANT] Container 'andip-qdrant' status: {state}")

    if state == "running":
        # It's running but port wasn't open yet, wait a moment
        time.sleep(2)
        return True

    elif state == "stopped":
        print("[QDRANT] Starting stopped container 'andip-qdrant'...")
        subprocess.run(["docker", "start", "andip-qdrant"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
    elif state == "missing":
        print("[QDRANT] Container not found. Creating and running new 'andip-qdrant' container...")
        cmd = [
            "docker", "run", "-d",
            "--name", "andip-qdrant",
            "-p", "6333:6333",
            "-p", "6033:6033",
            "-v", "qdrant_storage:/qdrant/storage",
            "qdrant/qdrant"
        ]
        subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # 3. Poll connection until open or timeout (15 seconds)
    print("[QDRANT] Waiting for Qdrant service to become active on localhost:6333...")
    for i in range(15):
        time.sleep(1)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            if s.connect_ex(("localhost", 6333)) == 0:
                print("[QDRANT] Qdrant is now successfully running!")
                return True
                
    print("[ERROR] Qdrant container started but port 6333 did not become responsive in time.")
    return False

def get_qdrant_client():
    """Lazily loads and returns the QdrantClient instance."""
    global _qdrant_client
    if _qdrant_client is not None:
        return _qdrant_client
        
    try:
        from qdrant_client import QdrantClient
        _qdrant_client = QdrantClient(host="localhost", port=6333, timeout=5)
        return _qdrant_client
    except ImportError:
        print("[ERROR] 'qdrant-client' package is not installed. Run 'pip install qdrant-client'.")
        return None

def get_embedding_model():
    """Lazily loads and returns the FastEmbed TextEmbedding model (dim = 384)."""
    global _embedding_model
    if _embedding_model is not None:
        return _embedding_model
        
    try:
        from fastembed import TextEmbedding
        print("[QDRANT] Initializing local FastEmbed model (BAAI/bge-small-en-v1.5)...")
        _embedding_model = TextEmbedding()
        return _embedding_model
    except Exception as e:
        print(f"[ERROR] Failed to initialize fastembed: {e}")
        return None

# Static component details library to seed the DB
COMPONENT_METADATA_REGISTRY = [
    {
        "id": "ImmersiveHero",
        "name": "Immersive Hero",
        "category": "hero",
        "description": "Luxury premium minimalist hero section with organic background blob animations, large serif headings, and high contrast magnetic call-to-actions. Excellent for high-end fashion, luxury brands, exclusive editorial portfolios, dark themes, and sophisticated storytelling.",
        "emotions": ["luxury", "mysterious", "calm", "editorial"],
        "archetypes": ["ruler", "magician", "creator"],
        "spatial_mode": "airy"
    },
    {
        "id": "SplitSectionHero",
        "name": "Split Section Hero",
        "category": "hero",
        "description": "Asymmetrical split screen hero section with distinct left and right panels sliding at different parallax speeds. Modern, editorial feel. Perfect for creative photography studios, lifestyle blogs, architectural portfolios, and bright minimalist sites.",
        "emotions": ["editorial", "calm", "luxury", "avant-garde"],
        "archetypes": ["creator", "explorer", "artist"],
        "spatial_mode": "asymmetric"
    },
    {
        "id": "BentoGrid",
        "name": "Bento Grid Showcase",
        "category": "showcase",
        "description": "Asymmetric Bento Grid layout with flexible CSS grid containers (span 2x2, 1x1, 2x1) showcasing items with subtle mouse hover glows, gradients, and framer-motion micro-interactions. High-tech luxurious portfolio showcase or detailed service presentation.",
        "emotions": ["editorial", "luxury", "cyberpunk", "modern"],
        "archetypes": ["creator", "ruler", "sage"],
        "spatial_mode": "grid-heavy"
    },
    {
        "id": "Marquee",
        "name": "Infinite Moving Marquee",
        "category": "utility",
        "description": "Infinite horizontally scrolling typographic marquee or logo banner. Performance-optimized pure CSS animation that pauses on mouse hover. Gives aggressive, street-style, fast-paced street culture energy, raw industrial vibes, or modern typography branding showcase.",
        "emotions": ["aggressive", "cyberpunk", "energetic", "playful"],
        "archetypes": ["outlaw", "hero", "jester"],
        "spatial_mode": "dense"
    },
    {
        "id": "ParallaxGallery",
        "name": "Parallax Depth Gallery",
        "category": "gallery",
        "description": "Immersive multi-layered depth gallery using GSAP ScrollTrigger to move images vertically at varying speeds (0.3x, 0.6x, 1x). Stunning parallax depth for visual portfolios, premium editorial showcases, and luxurious art directions.",
        "emotions": ["luxury", "calm", "editorial", "avant-garde"],
        "archetypes": ["creator", "magician", "explorer"],
        "spatial_mode": "airy"
    },
    {
        "id": "TextReveal",
        "name": "Scroll Reveal Manifesto Text",
        "category": "text",
        "description": "Scroll-triggered text reveal effect using GSAP ScrollTrigger to reveal sentences or manifestos word-by-word with transition of opacity and blur. Dramatic, immersive branding statements, editorial story sections, and premium brand storytelling.",
        "emotions": ["luxury", "mysterious", "calm", "editorial"],
        "archetypes": ["ruler", "sage", "magician"],
        "spatial_mode": "airy"
    },
    {
        "id": "TestimonialCarousel",
        "name": "Testimonial Swipe Carousel",
        "category": "reviews",
        "description": "Clean, responsive client review testimonial slider powered by Embla Carousel headless API. Supports touch swipe, drag, autoplay, and dots indicator. Builds deep social proof and solid trust beautifully.",
        "emotions": ["trustworthy", "calm", "friendly"],
        "archetypes": ["everyman", "caregiver", "ruler"],
        "spatial_mode": "standard"
    },
    {
        "id": "StatsCounter",
        "name": "Spring Stats Counter",
        "category": "metrics",
        "description": "Dynamic animated count-up numerical statistics stats counter. Triggers automatically when entering viewport using Framer Motion springs and scroll view. Excellent for business impact metrics, achievements, and reliability statistics.",
        "emotions": ["trustworthy", "energetic", "professional"],
        "archetypes": ["hero", "ruler", "sage"],
        "spatial_mode": "standard"
    },
    {
        "id": "ScrollPinSection",
        "name": "GSAP Scroll Pin Showcase",
        "category": "narrative",
        "description": "Immersive narrative showcase using GSAP ScrollTrigger pin & scrub pattern. Viewport freezes, and scrolling reveals sequential content cards or progressive steps. Perfect for product features, timelines, premium story workflows.",
        "emotions": ["luxury", "mysterious", "cyberpunk", "energetic"],
        "archetypes": ["magician", "creator", "hero"],
        "spatial_mode": "immersive"
    },
    {
        "id": "FeatureGrid",
        "name": "Feature Staggered Grid",
        "category": "showcase",
        "description": "Modern card grid showcasing features or services with staggered reveal entry animations using Framer Motion and hover scale micro-animations. Highly versatile, robust, clean and trustworthy list layout.",
        "emotions": ["trustworthy", "calm", "professional"],
        "archetypes": ["everyman", "caregiver", "sage"],
        "spatial_mode": "grid-heavy"
    },
    {
        "id": "InteractiveGallery",
        "name": "GSAP Horizontal Scroll Gallery",
        "category": "gallery",
        "description": "Horizontal photo gallery showcase that slides sideways on vertical scroll using GSAP. Great for immersive photography studios, fashion highlights, visual galleries, and high-fidelity portfolios.",
        "emotions": ["editorial", "luxury", "playful"],
        "archetypes": ["creator", "artist", "explorer"],
        "spatial_mode": "asymmetric"
    },
    {
        "id": "MotionCTA",
        "name": "Motion Glow CTA",
        "category": "cta",
        "description": "Animated Call to Action CTA section with premium background glow gradients, magnetic hover button effects, and responsive visual layouts. Captivating closing statement and action buttons.",
        "emotions": ["energetic", "trustworthy", "luxury"],
        "archetypes": ["hero", "ruler", "creator"],
        "spatial_mode": "standard"
    },
    {
        "id": "GlassmorphicFooter",
        "name": "Glassmorphic Footer",
        "category": "footer",
        "description": "Beautiful modern footer with soft background glassmorphism, social media icon hover animations, clear layout structure, and neat site directory links.",
        "emotions": ["luxury", "calm", "modern"],
        "archetypes": ["everyman", "ruler"],
        "spatial_mode": "standard"
    }
]

def initialize_components_registry(force_recreate: bool = False) -> bool:
    """
    Creates and populates the Qdrant components_registry collection.
    Loads actual JSX code from disk and saves it into the payload.
    Consolidates baseline physical templates and programmatic expanded database.
    """
    try:
        try:
            from execution.seed_expanded_components import seed_database
        except ImportError:
            from seed_expanded_components import seed_database
        print("[QDRANT] Delegating initialization to seed_expanded_components...")
        return seed_database()
    except Exception as e:
        print(f"[QDRANT WARNING] Failed to delegate seeding: {e}. Falling back to baseline static seeding...")
        
    if not ensure_qdrant_running():
        return False
        
    client = get_qdrant_client()
    model = get_embedding_model()
    if not client or not model:
        return False
        
    collection_name = "components_registry"
    
    # Check if exists
    try:
        collections = client.get_collections()
        exists = any(c.name == collection_name for c in collections.collections)
    except Exception as e:
        print(f"[QDRANT] Failed to fetch collections: {e}")
        return False
        
    if exists and not force_recreate:
        print(f"[QDRANT] Collection '{collection_name}' already exists. Skipping initialization.")
        return True
        
    if exists and force_recreate:
        print(f"[QDRANT] Force recreating collection '{collection_name}'...")
        client.delete_collection(collection_name)
        
    # Create collection
    # FastEmbed 'BAAI/bge-small-en-v1.5' outputs 384 dimensions
    from qdrant_client.models import Distance, VectorParams
    try:
        client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=384, distance=Distance.COSINE),
        )
        print(f"[QDRANT] Collection '{collection_name}' created successfully.")
    except Exception as e:
        print(f"[ERROR] Could not create Qdrant collection: {e}")
        return False
        
    # Prepare documents for seeding
    documents = []
    ids = []
    payloads = []
    
    for idx, comp in enumerate(COMPONENT_METADATA_REGISTRY):
        comp_id = comp["id"]
        # Load JSX code if exists
        jsx_file = TEMPLATES_DIR / f"{comp_id}.jsx"
        jsx_code = ""
        if jsx_file.exists():
            jsx_code = jsx_file.read_text(encoding="utf-8")
        else:
            # Check fallback SplitSectionHero
            if comp_id == "SplitSectionHero" and (TEMPLATES_DIR / "SplitSection.jsx").exists():
                jsx_code = (TEMPLATES_DIR / "SplitSection.jsx").read_text(encoding="utf-8")
                
        # Text representation for embedding
        embedding_text = f"Component ID: {comp_id}\n"
        embedding_text += f"Name: {comp['name']}\n"
        embedding_text += f"Description: {comp['description']}\n"
        embedding_text += f"Target Emotions: {', '.join(comp['emotions'])}\n"
        embedding_text += f"Target Archetypes: {', '.join(comp['archetypes'])}\n"
        embedding_text += f"Spatial Layout Mode: {comp['spatial_mode']}"
        
        documents.append(embedding_text)
        ids.append(idx)
        
        payloads.append({
            "id": comp_id,
            "name": comp["name"],
            "category": comp["category"],
            "description": comp["description"],
            "emotions": comp["emotions"],
            "archetypes": comp["archetypes"],
            "spatial_mode": comp["spatial_mode"],
            "jsx_code": jsx_code
        })
        
    print(f"[QDRANT] Seeding {len(documents)} components into collection...")
    
    # Generate embeddings
    try:
        embeddings = list(model.embed(documents))
        
        # Upload to Qdrant
        from qdrant_client.models import PointStruct
        points = []
        for i, vector in enumerate(embeddings):
            # Convert numpy array to list
            vec_list = vector.tolist() if hasattr(vector, "tolist") else list(vector)
            points.append(PointStruct(
                id=ids[i],
                vector=vec_list,
                payload=payloads[i]
            ))
            
        client.upsert(collection_name=collection_name, points=points)
        print("[QDRANT] Database seeded and indexed successfully!")
        return True
    except Exception as e:
        print(f"[ERROR] Failed to seed Qdrant database: {e}")
        return False

def search_components(query: str, limit: int = 5) -> list:
    """
    Performs a semantic vector search in Qdrant based on user prompt or design tokens.
    Returns a list of matching components with scores.
    """
    if not ensure_qdrant_running():
        print("[QDRANT] Qdrant not running. Search returning empty list (triggers fallback).")
        return []
        
    client = get_qdrant_client()
    model = get_embedding_model()
    if not client or not model:
        return []
        
    collection_name = "components_registry"
    
    try:
        # Check collection exists
        collections = client.get_collections()
        exists = any(c.name == collection_name for c in collections.collections)
        if not exists:
            # Try initializing first
            if not initialize_components_registry():
                return []
                
        # Generate embedding for query
        query_vectors = list(model.embed([query]))
        query_vector = query_vectors[0].tolist() if hasattr(query_vectors[0], "tolist") else list(query_vectors[0])
        
        # Search Qdrant
        response = client.query_points(
            collection_name=collection_name,
            query=query_vector,
            limit=limit
        )
        hits = response.points
        
        results = []
        for hit in hits:
            payload = hit.payload
            results.append({
                "id": payload.get("id"),
                "name": payload.get("name"),
                "category": payload.get("category"),
                "description": payload.get("description"),
                "emotions": payload.get("emotions"),
                "archetypes": payload.get("archetypes"),
                "spatial_mode": payload.get("spatial_mode"),
                "jsx_code": payload.get("jsx_code"),
                "score": hit.score
            })
        return results
    except Exception as e:
        print(f"[ERROR] Qdrant search encountered an error: {e}")
        return []

if __name__ == "__main__":
    print("Checking and initializing Qdrant database...")
    success = initialize_components_registry(force_recreate=True)
    if success:
        print("\nTesting semantic search...")
        test_query = "luxurious gold aesthetic organic animations"
        matches = search_components(test_query, limit=3)
        print(f"Query: '{test_query}'")
        for m in matches:
            print(f"- {m['name']} (Score: {m['score']:.4f})")
    else:
        print("Initialization failed.")
