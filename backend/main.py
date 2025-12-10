import os
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from backend.models import (
    UploadResponse,
    QuestionRequest,
    AnswerResponse,
    HealthResponse,
)
from backend.rag_engine import RAGEngine

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="JEE Textbook Q&A API",
    description="RAG-based system for JEE Physics textbook question answering",
    version="1.0.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize RAG engine with multi-provider support
groq_api_key = os.getenv("GROQ_API_KEY")
gemini_api_key = os.getenv("GEMINI_API_KEY")

if not groq_api_key and not gemini_api_key:
    raise ValueError("Please provide either GROQ_API_KEY or GEMINI_API_KEY in .env file")

rag_engine = RAGEngine(gemini_api_key=gemini_api_key, groq_api_key=groq_api_key)

# Load default book if it exists AND if it's not already in the database
DEFAULT_BOOK_PATH = "default_books/default_book.pdf"
if os.path.exists(DEFAULT_BOOK_PATH):
    try:
        # Check if default book is already loaded
        stats = rag_engine.get_stats()
        has_book = rag_engine.has_document("default_book.pdf")
        
        if has_book:
            print(f"✓ Default book already loaded from database: {stats['documents_count']} chunks")
        else:
            if stats['documents_count'] > 0:
                print(f"⚠️  Found {stats['documents_count']} chunks in DB, but not from default_book.pdf")
                print(f"   Re-processing default book...")
            else:
                print(f"📚 No cached data found. Processing default book for the first time...")
            
            print(f"Loading default book from {DEFAULT_BOOK_PATH}...")
            with open(DEFAULT_BOOK_PATH, "rb") as f:
                content = f.read()
            result = rag_engine.process_pdf(content, "default_book.pdf")
            print(f"✓ Default book loaded: {result['pages']} pages, {result['chunks']} chunks")
    except Exception as e:
        print(f"⚠ Warning: Could not load default book: {str(e)}")
else:
    print(f"ℹ No default book found at {DEFAULT_BOOK_PATH}")



@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "JEE Textbook Q&A API",
        "docs": "/docs",
        "health": "/health",
    }


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Check system health and stats"""
    try:
        stats = rag_engine.get_stats()
        return HealthResponse(
            status="healthy",
            documents_count=stats["documents_count"],
            model=stats["model"],
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/book-status")
async def get_book_status():
    """Get information about the currently loaded book"""
    try:
        stats = rag_engine.get_stats()
        has_default_book = os.path.exists(DEFAULT_BOOK_PATH)
        
        return {
            "has_default_book": has_default_book,
            "default_book_name": "default_book.pdf" if has_default_book else None,
            "documents_loaded": stats["documents_count"] > 0,
            "total_chunks": stats["documents_count"],
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@app.post("/upload", response_model=UploadResponse)
async def upload_pdf(file: UploadFile = File(...)):
    """Upload and process a PDF file"""
    try:
        # Validate file type
        if not file.filename.lower().endswith(".pdf"):
            raise HTTPException(
                status_code=400, detail="Only PDF files are allowed"
            )

        # Read file content
        content = await file.read()

        # Process PDF
        result = rag_engine.process_pdf(content, file.filename)

        return UploadResponse(
            message="PDF processed successfully",
            filename=file.filename,
            pages=result["pages"],
            chunks=result["chunks"],
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error processing PDF: {str(e)}"
        )


@app.post("/ask", response_model=AnswerResponse)
async def ask_question(request: QuestionRequest):
    """Ask a question about the uploaded PDF"""
    try:
        # Directly run RAG pipeline; if nothing in DB,
        # the engine will return a friendly message.
        result = rag_engine.ask(request.question)

        return AnswerResponse(
            question=request.question,
            answer=result["answer"],
            sources=result["sources"],
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error answering question: {str(e)}"
        )


@app.delete("/clear")
async def clear_documents():
    """Clear all stored documents"""
    try:
        rag_engine.clear()
        return {"message": "All documents cleared successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error clearing documents: {str(e)}"
        )


# Optional debug endpoint to verify stored docs
@app.get("/debug/chroma")
async def debug_chroma():
    try:
        items = rag_engine.collection.get()
        return {"count": len(items.get("ids", []))}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
