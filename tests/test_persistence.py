"""
Test script to verify ChromaDB persistence optimization
"""
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.rag_engine import RAGEngine
from dotenv import load_dotenv

load_dotenv()

def test_persistence():
    print("=" * 60)
    print("Testing ChromaDB Persistence Optimization")
    print("=" * 60)
    
    # Initialize RAG engine
    groq_api_key = os.getenv("GROQ_API_KEY")
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    
    print("\n1. Initializing RAG Engine...")
    engine = RAGEngine(gemini_api_key=gemini_api_key, groq_api_key=groq_api_key)
    
    # Check stats
    stats = engine.get_stats()
    print(f"\n2. Current Database Stats:")
    print(f"   - Documents: {stats['documents_count']}")
    print(f"   - Model: {stats['model']}")
    
    # Check if default book is loaded
    has_default = engine.has_document("default_book.pdf")
    print(f"\n3. Default Book Status:")
    print(f"   - Has default_book.pdf: {has_default}")
    
    if has_default:
        print("\n✅ SUCCESS: Default book is already in database!")
        print("   Server will start FAST on next restart (no re-processing needed)")
    else:
        print("\n⚠️  Default book not found in database")
        print("   First startup will process the book and cache embeddings")
    
    # Check database directory
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, "..", "backend", "chroma_db")
    db_exists = os.path.exists(db_path)
    
    print(f"\n4. Database Directory:")
    print(f"   - Path: {db_path}")
    print(f"   - Exists: {db_exists}")
    
    if db_exists:
        # Get size of database
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(db_path):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                total_size += os.path.getsize(filepath)
        
        size_mb = total_size / (1024 * 1024)
        print(f"   - Size: {size_mb:.2f} MB")
    
    print("\n" + "=" * 60)
    print("Test Complete!")
    print("=" * 60)

if __name__ == "__main__":
    test_persistence()
