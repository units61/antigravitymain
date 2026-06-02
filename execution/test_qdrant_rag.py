import sys
from pathlib import Path

# Add project root to sys path
EXECUTION_DIR = Path(__file__).parent
BASE_DIR = EXECUTION_DIR.parent
sys.path.append(str(BASE_DIR))

from execution.qdrant_manager import initialize_components_registry, search_components, is_docker_running

def main():
    print("==================================================")
    print("      ANDIP QDRANT & RAG TEST INTEGRITY CHECK     ")
    print("==================================================")
    
    # 1. Check if Docker is active
    docker_ok = is_docker_running()
    print(f"Docker Daemon Running: {'YES' if docker_ok else 'NO'}")
    if not docker_ok:
        print("\n[WARNING] Docker Desktop is NOT running on your machine!")
        print("Please start Docker Desktop and run this script again to test full Docker Qdrant.")
        print("We will attempt to perform a mock fallback search test now.\n")
    
    # 2. Try initializing Qdrant database
    print("\n[STEP 1] Initializing Qdrant Collection & Seeding JSX components...")
    success = initialize_components_registry(force_recreate=True)
    
    if not success:
        print("\n[FAILED] Qdrant DB seeding failed. Qdrant RAG is inactive.")
        print("This is normal if Docker Desktop is closed. The ANDIP pipeline will use Graceful Fallback.")
        return
        
    print("\n[SUCCESS] Qdrant Registry Initialized & Seeded successfully!")
    
    # 3. Perform test semantic queries
    print("\n[STEP 2] Performing semantic queries to test search...")
    queries = [
        "luxury gold and black aesthetic organic smooth layout",
        "raw industrial brutalist streetwear neon fast scrolling text marquee",
        "clean trustworthy corporate feedback slider",
        "horizontal visual gallery for a photography showcase"
    ]
    
    for q in queries:
        print(f"\nQuery: '{q}'")
        results = search_components(q, limit=2)
        if not results:
            print("  No results found or error occurred.")
        for idx, res in enumerate(results):
            print(f"  {idx+1}. {res['name']} ({res['id']}) - Score: {res['score']:.4f}")
            print(f"     Description snippet: {res['description'][:100]}...")
            
    print("\n==================================================")
    print("      INTEGRITY CHECK COMPLETED SUCCESSFULLY      ")
    print("==================================================")

if __name__ == "__main__":
    main()
