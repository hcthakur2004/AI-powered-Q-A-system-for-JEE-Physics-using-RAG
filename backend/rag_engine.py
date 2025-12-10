import os
from io import BytesIO
from typing import List, Dict, Tuple

import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
import google.generativeai as genai
from groq import Groq
import PyPDF2


class RAGEngine:
    def __init__(self, gemini_api_key: str = None, groq_api_key: str = None):
        """Initialize RAG engine with embeddings model, vector database, and AI provider"""

        # ✅ Load Embedding Model
        print("Loading embedding model...")
        self.embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

        # ✅ Initialize ChromaDB with PERSISTENT STORAGE
        print("Initializing ChromaDB...")
        base_dir = os.path.dirname(os.path.abspath(__file__))
        persist_dir = os.path.join(base_dir, "chroma_db")

        # Use PersistentClient for automatic persistence (newer ChromaDB API)
        self.chroma_client = chromadb.PersistentClient(
            path=persist_dir,
            settings=Settings(
                anonymized_telemetry=False,
                allow_reset=True,
            )
        )

        self.collection = self.chroma_client.get_or_create_collection(
            name="pdf_documents",
            metadata={"hnsw:space": "cosine"},
        )

        # ✅ Initialize AI Provider (Groq or Gemini)
        self.ai_provider = None
        self.model_name = None
        
        # Try Groq first (FREE, FAST, and GENEROUS LIMITS)
        if groq_api_key:
            try:
                print("Initializing Groq AI (FREE & FAST)...")
                self.groq_client = Groq(api_key=groq_api_key)
                self.ai_provider = "groq"
                self.model_name = "llama-3.3-70b-versatile"  # Free, powerful model
                print(f"✅ Groq AI loaded: {self.model_name}")
                print("   🎉 Using FREE Groq API - No quota limits!")
            except Exception as e:
                print(f"⚠️ Groq initialization failed: {e}")
        
        # Fallback to Gemini if Groq not available
        if not self.ai_provider and gemini_api_key:
            print("Initializing Gemini AI...")
            genai.configure(api_key=gemini_api_key)
            
            # Try Gemini models in order
            models_to_try = [
                "gemini-1.5-flash",      # Fastest, most generous free tier
                "gemini-1.5-pro",        # More capable
                "gemini-pro"             # Fallback
            ]
            
            for model_name in models_to_try:
                try:
                    self.gemini_model = genai.GenerativeModel(model_name)
                    self.ai_provider = "gemini"
                    self.model_name = model_name
                    print(f"✅ Gemini model loaded: {model_name}")
                    break
                except Exception as e:
                    print(f"⚠️ {model_name} not available: {e}")
                    if model_name == models_to_try[-1]:
                        raise Exception("No AI models available!")
        
        if not self.ai_provider:
            raise Exception("No AI provider available! Please provide GROQ_API_KEY or GEMINI_API_KEY")

        # Debug: how many docs are already in DB
        try:
            existing_items = self.collection.get()
            print("📌 Loaded documents from DB:", len(existing_items.get("ids", [])))
        except Exception as e:
            print("⚠️ Error loading persisted data:", e)

        print("✅ RAG Engine initialized successfully!")

    # ---------------------------------------------------
    # PDF PROCESSING
    # ---------------------------------------------------

    def extract_text_from_pdf(self, pdf_file: bytes) -> Tuple[str, int]:
        """Extract text from PDF file"""
        pdf_reader = PyPDF2.PdfReader(BytesIO(pdf_file))
        text = ""
        pages = len(pdf_reader.pages)

        for page in pdf_reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n\n"

        return text.strip(), pages

    def chunk_text(
        self, text: str, chunk_size: int = 500, overlap: int = 50
    ) -> List[str]:
        """Split text into overlapping chunks"""
        words = text.split()
        chunks: List[str] = []

        for i in range(0, len(words), chunk_size - overlap):
            chunk = " ".join(words[i : i + chunk_size])
            if chunk.strip():
                chunks.append(chunk)

        return chunks

    def process_pdf(self, pdf_file: bytes, filename: str) -> Dict:
        """Process PDF: extract text, create chunks, generate embeddings, store in DB"""

        file_size_mb = len(pdf_file) / (1024 * 1024)
        print(f"📄 Processing PDF: {filename} ({file_size_mb:.2f} MB)")

        # ✅ Extract text
        print("📖 Extracting text from PDF...")
        text, pages = self.extract_text_from_pdf(pdf_file)
        print(f"✅ Extracted {len(text)} characters from {pages} pages")

        # ✅ Create chunks
        print("✂️ Creating text chunks...")
        chunks = self.chunk_text(text)
        print(f"✅ Created {len(chunks)} chunks")

        if not chunks:
            return {"pages": pages, "chunks": 0}

        # ✅ Generate embeddings (this may take time for large files)
        print(f"🧠 Generating embeddings for {len(chunks)} chunks...")
        print("   (This may take 1-2 minutes for large files...)")
        embeddings = self.embedding_model.encode(chunks, show_progress_bar=False).tolist()
        print("✅ Embeddings generated!")

        # ✅ Clear old documents
        try:
            existing_items = self.collection.get()
            if existing_items.get("ids"):
                self.collection.delete(ids=existing_items["ids"])
        except Exception as e:
            print(f"Note: Collection clear skipped: {e}")

        # ✅ Store in ChromaDB
        ids = [f"chunk_{i}" for i in range(len(chunks))]
        metadatas = [
            {
                "filename": filename,
                "chunk_id": i,
                "page": i // 3,
            }
            for i in range(len(chunks))
        ]

        self.collection.add(
            embeddings=embeddings,
            documents=chunks,
            ids=ids,
            metadatas=metadatas,
        )

        # ✅ Data is automatically persisted with PersistentClient

        return {
            "pages": pages,
            "chunks": len(chunks),
        }

    # ---------------------------------------------------
    # RETRIEVAL
    # ---------------------------------------------------

    def retrieve_context(
        self, question: str, n_results: int = 5
    ) -> Tuple[List[str], List[dict]]:
        """Retrieve relevant context chunks for a question"""

        query_embedding = self.embedding_model.encode([question]).tolist()

        results = self.collection.query(
            query_embeddings=query_embedding, n_results=n_results
        )

        contexts = results.get("documents", [[]])[0]
        metadatas = results.get("metadatas", [[]])[0]

        return contexts, metadatas

    # ---------------------------------------------------
    # AI GENERATION (Multi-Provider)
    # ---------------------------------------------------

    def generate_answer(self, question: str, contexts: List[str]) -> str:
        """Generate answer using available AI provider (Groq or Gemini)"""

        if not contexts:
            return (
                "I couldn't find relevant information in the document to answer your question."
            )

        context_text = "\n\n".join(
            [f"Context {i + 1}:\n{ctx}" for i, ctx in enumerate(contexts)]
        )

        prompt = f"""You are a helpful AI assistant. Answer the question based ONLY on the provided document context.

Context:
{context_text}

Question:
{question}

Rules:
- Use only the document context
- If insufficient data, clearly state so
- Be concise and accurate

Answer:"""

        try:
            if self.ai_provider == "groq":
                # Use Groq API (FREE & FAST)
                response = self.groq_client.chat.completions.create(
                    model=self.model_name,
                    messages=[
                        {"role": "system", "content": "You are a helpful AI assistant that answers questions based on provided context."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.3,
                    max_tokens=1024
                )
                return response.choices[0].message.content
            
            elif self.ai_provider == "gemini":
                # Use Gemini API
                response = self.gemini_model.generate_content(prompt)
                return response.text
            
        except Exception as e:
            return f"Error generating answer: {str(e)}"

    # ---------------------------------------------------
    # FULL RAG PIPELINE
    # ---------------------------------------------------

    def ask(self, question: str) -> Dict:
        """Complete RAG pipeline: retrieve context and generate answer"""

        contexts, metadatas = self.retrieve_context(question)
        answer = self.generate_answer(question, contexts)

        sources = [
            {
                "text": ctx[:200] + "..." if len(ctx) > 200 else ctx,
                "page": meta.get("page", 0),
                "chunk_id": meta.get("chunk_id", 0),
            }
            for ctx, meta in zip(contexts, metadatas)
        ]

        return {
            "answer": answer,
            "sources": sources,
        }

    # ---------------------------------------------------
    # SYSTEM STATS & CLEANUP
    # ---------------------------------------------------

    def get_stats(self) -> Dict:
        """Get statistics about stored documents"""
        try:
            existing_items = self.collection.get()
            count = len(existing_items.get("ids", []))
        except Exception:
            count = 0

        return {
            "documents_count": count,
            "model": f"{self.ai_provider}:{self.model_name}",
            "provider": self.ai_provider
        }

    def has_document(self, filename: str) -> bool:
        """Check if a specific document is already loaded in the database"""
        try:
            existing_items = self.collection.get()
            if existing_items.get("metadatas"):
                return any(
                    meta.get("filename") == filename 
                    for meta in existing_items["metadatas"]
                )
        except Exception:
            pass
        return False

    def clear(self):
        """Clear all stored documents"""
        try:
            existing_items = self.collection.get()
            if existing_items.get("ids"):
                self.collection.delete(ids=existing_items["ids"])
            # Data is automatically persisted with PersistentClient
        except Exception as e:
            print(f"Note: Collection was empty or error clearing: {e}")
