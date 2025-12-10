# 📚 JEE Textbook Q&A

A powerful **RAG (Retrieval Augmented Generation)** system for JEE Physics students. Ask questions about Halliday-Resnick-Walker's "Fundamentals of Physics" and get accurate, AI-powered answers based strictly on the textbook content. Built with FastAPI, React, ChromaDB, and powered by Groq AI.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.9+-blue.svg)
![React](https://img.shields.io/badge/react-18+-blue.svg)

---

## ✨ Features

### Core Functionality
- 📚 **Preloaded Physics Textbook** - Halliday-Resnick-Walker "Fundamentals of Physics" (11th Edition, Class 11) ready to query instantly
- 📄 **PDF Upload & Processing** - Upload any PDF document for intelligent analysis
- 💬 **Natural Language Q&A** - Ask questions in plain English, get accurate answers
- 🎯 **Context-Aware Answers** - Responses based strictly on document content
- 📍 **Source Citations** - See which parts of the document were used for each answer

### AI & Performance
- 🤖 **Multi-AI Support** - Choose between Groq (FREE & FAST) or Google Gemini
- 🧠 **Smart Embeddings** - Uses sentence-transformers for semantic understanding
- 🔍 **Vector Search** - ChromaDB for efficient similarity search
- ⚡ **Lightning Fast** - Optimized RAG pipeline for quick responses
- 🚀 **Persistent Cache** - Embeddings cached for **95% faster startup** (2min → 5sec)
- 🆓 **100% Free Option** - Use Groq API with generous limits (no credit card needed!)

### User Experience
- 🌙 **Dark Mode** - Beautiful light and dark themes with smooth transitions
- 💎 **Modern UI** - Dumroo.ai-inspired design with glassmorphism effects
- 📱 **Responsive** - Works seamlessly on desktop and mobile
- 🎨 **Beautiful Animations** - Smooth transitions and micro-interactions

---

## 🏗️ Tech Stack

### Backend
| Technology | Purpose |
|------------|---------|
| **FastAPI** | High-performance Python web framework |
| **ChromaDB** | Vector database for embeddings storage |
| **Sentence-Transformers** | State-of-the-art text embeddings (all-MiniLM-L6-v2) |
| **PyPDF2** | PDF text extraction |
| **Groq API** | FREE, ultra-fast AI (Llama 3.3 70B) - **RECOMMENDED** |
| **Google Gemini** | Alternative AI provider (Gemini 1.5 Flash/Pro) |

### Frontend
| Technology | Purpose |
|------------|---------|
| **React 18** | Modern UI library |
| **Vite** | Lightning-fast build tool |
| **Vanilla CSS** | Custom styling with glassmorphism |
| **Fetch API** | Clean API communication |

---

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.9+** ([Download](https://www.python.org/downloads/))
- **Node.js 16+** ([Download](https://nodejs.org/))
- **FREE Groq API Key** ([Get instantly](https://console.groq.com/keys)) - **RECOMMENDED**
  - OR **Google Gemini API Key** ([Get here](https://makersuite.google.com/app/apikey))

> 💡 **Tip**: Groq is recommended because it's completely free, has no quota limits, and is incredibly fast!

---

## 🚀 Installation & Setup

### 1️⃣ Clone the Repository

```bash
git clone <your-repo-url>
cd "ai pdf"
```

### 2️⃣ Backend Setup

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
.\venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3️⃣ Configure Environment Variables

Create a `.env` file in the **root directory**:

**Option A: Groq (RECOMMENDED - FREE & FAST)** ⚡
```env
GROQ_API_KEY=gsk_your_groq_api_key_here
```
👉 Get your FREE key at: https://console.groq.com/keys (No credit card needed!)

**Option B: Gemini (Has quota limits)**
```env
GEMINI_API_KEY=your_gemini_api_key_here
```

**Option C: Both (Groq will be used first)**
```env
GROQ_API_KEY=gsk_your_groq_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here
```

### 4️⃣ Frontend Setup

```bash
cd frontend
npm install
cd ..
```

---

## 🎮 Running the Application

You need **two terminal windows** to run both backend and frontend:

### Terminal 1: Start Backend

```bash
# From root directory
.\venv\Scripts\activate  # Windows
# source venv/bin/activate  # macOS/Linux

python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

**Expected output:**
```
✅ Groq AI loaded: llama-3.3-70b-versatile
📌 Loaded documents from DB: 2217
✅ RAG Engine initialized successfully!
✓ Default book already loaded from database: 2217 chunks
INFO:     Application startup complete.
```

### Terminal 2: Start Frontend

```bash
cd frontend
npm run dev
```

**Expected output:**
```
  VITE v5.x.x  ready in xxx ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
```

### 🌐 Access the Application

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs (Interactive Swagger UI)

---

## 📖 Usage Guide

### Option 1: Use Preloaded Physics Textbook (Ready to Use!)

**This system comes with Halliday-Resnick-Walker "Fundamentals of Physics" (11th Edition) already loaded!**

Perfect for Class 11 Physics students who want instant access to their textbook!

1. **Just Start Asking**: The book is already loaded - no upload needed!
2. **Example Questions**:
   - "What is Newton's second law of motion?"
   - "Explain the concept of work and energy"
   - "What are the laws of thermodynamics?"
   - "Derive the equation for projectile motion"

**Book Details:**
- **Title**: Fundamentals of Physics
- **Authors**: Halliday, Resnick, Walker
- **Edition**: 11th Edition
- **Pages**: 1,452 pages
- **Chunks**: 2,217 searchable chunks
- **Coverage**: Complete Class 11 Physics syllabus

**Want to use your own book?** Replace `default_books/default_book.pdf` with your PDF, delete `backend/chroma_db/`, and restart the server.

### Option 2: Upload PDFs Manually

Perfect for one-time document analysis or multiple different documents!

1. **Upload PDF**: Click the upload area or drag & drop a PDF file
2. **Wait for Processing**: The system will extract text and create embeddings
3. **Ask Questions**: Type your question in the input field
4. **Get Answers**: Receive AI-generated answers with source citations

### Option 3: Combine Both

The best of both worlds!

- Keep your main textbook as the default book
- Upload additional PDFs (notes, papers, etc.) as needed
- Ask questions from all loaded books together!

---

## 🔄 How It Works

```
┌─────────────┐
│  PDF Upload │
└──────┬──────┘
       │
       ▼
┌─────────────────┐
│ Text Extraction │  (PyPDF2)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Text Chunking   │  (500 words, 50 overlap)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Generate        │  (Sentence-Transformers)
│ Embeddings      │  all-MiniLM-L6-v2
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Store in        │  (ChromaDB)
│ Vector DB       │  Persistent Storage
└────────┬────────┘
         │
         ▼
    ┌────────┐
    │ Ready! │
    └────────┘

When you ask a question:
┌──────────────┐
│ Your Question│
└──────┬───────┘
       │
       ▼
┌─────────────────┐
│ Embed Question  │  (Same model)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Vector Search   │  (Find top 5 similar chunks)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ AI Generation   │  (Groq/Gemini)
│ with Context    │  Answer based on retrieved chunks
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Answer + Sources│
└─────────────────┘
```

---

## ⚡ Performance Optimization

The system includes **smart embedding caching** that dramatically improves startup time:

### Startup Time Comparison

| Scenario | Before Optimization | After Optimization | Improvement |
|----------|--------------------|--------------------|-------------|
| **First Startup** | ~2 minutes | ~2 minutes | Same (needs processing) |
| **Restart #1** | ~2 minutes | **~5 seconds** | **96% faster** ⚡ |
| **Restart #2+** | ~2 minutes | **~5 seconds** | **96% faster** ⚡ |

### How It Works

1. **First Startup** (with default book):
   - Loads and processes the PDF
   - Generates embeddings (~1-2 minutes for large files)
   - Saves to `backend/chroma_db/`
   - ✅ Ready to answer questions

2. **Subsequent Startups**:
   - Checks if default book is already in database
   - Loads existing embeddings from disk (~5 seconds)
   - ✅ Ready to answer questions immediately

### Database Location

- **Path**: `backend/chroma_db/`
- **Persistence**: Automatic with PersistentClient
- **Size**: ~10-20 MB (contains all embeddings)

### Force Re-processing (if needed)

**Option 1**: Delete the database folder
```bash
rm -rf backend/chroma_db
```

**Option 2**: Use the clear endpoint
```bash
curl -X DELETE http://localhost:8000/clear
```

Then restart the server.

📖 See [EMBEDDING_CACHE_OPTIMIZATION.md](EMBEDDING_CACHE_OPTIMIZATION.md) for technical details

---

## 🛠️ API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Root endpoint with API info |
| `GET` | `/health` | System health check and stats |
| `GET` | `/book-status` | Check if default book is loaded |
| `POST` | `/upload` | Upload and process a PDF file |
| `POST` | `/ask` | Ask a question about loaded documents |
| `DELETE` | `/clear` | Clear all stored documents |
| `GET` | `/docs` | Interactive API documentation (Swagger UI) |

### Example API Usage

**Upload a PDF:**
```bash
curl -X POST "http://localhost:8000/upload" \
  -F "file=@document.pdf"
```

**Ask a Question:**
```bash
curl -X POST "http://localhost:8000/ask" \
  -H "Content-Type: application/json" \
  -d '{"question": "What is the main topic of this document?"}'
```

**Check Health:**
```bash
curl http://localhost:8000/health
```

---

## 📁 Project Structure

```
ai pdf/
├── backend/
│   ├── main.py                 # FastAPI application & endpoints
│   ├── rag_engine.py           # RAG logic & ChromaDB integration
│   ├── models.py               # Pydantic data models
│   └── chroma_db/              # Persistent vector database (auto-created)
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx             # Main React component
│   │   └── index.css           # Styles (glassmorphism, dark mode)
│   ├── index.html              # HTML entry point
│   ├── package.json            # Frontend dependencies
│   └── vite.config.js          # Vite configuration
│
├── default_books/
│   ├── default_book.pdf        # Your default book (optional)
│   └── README.md               # Instructions for default books
│
├── tests/
│   └── test_persistence.py     # Test script for cache optimization
│
├── .env                        # Environment variables (API keys)
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── FREE_API_SETUP.md           # Detailed API setup guide
├── HOW_TO_ADD_DEFAULT_BOOK.md  # Default book setup guide
├── EMBEDDING_CACHE_OPTIMIZATION.md  # Technical optimization docs
└── OPTIMIZATION_VISUAL_GUIDE.md     # Visual optimization guide
```

---

## 🐛 Troubleshooting

### Backend Issues

**Problem**: `ModuleNotFoundError` or import errors
```bash
# Solution: Ensure virtual environment is activated and dependencies installed
.\venv\Scripts\activate
pip install -r requirements.txt
```

**Problem**: API key errors
```bash
# Solution: Check .env file exists and has valid API key
# Verify with:
cat .env  # macOS/Linux
type .env  # Windows
```

**Problem**: ChromaDB errors
```bash
# Solution: Delete and recreate the database
rm -rf backend/chroma_db
# Restart the server
```

**Problem**: Slow startup even after optimization
```bash
# Solution: Verify database exists
ls backend/chroma_db  # Should show files
# If empty, delete and let it regenerate
```

### Frontend Issues

**Problem**: `npm install` fails
```bash
# Solution: Clear cache and reinstall
npm cache clean --force
rm -rf node_modules package-lock.json
npm install
```

**Problem**: CORS errors
```bash
# Solution: Ensure backend is running on port 8000
# Check backend logs for CORS middleware initialization
```

**Problem**: API connection refused
```bash
# Solution: Verify backend is running
curl http://localhost:8000/health
```

### PDF Processing Issues

**Problem**: PDF upload fails
- **Solution**: Ensure PDF is not password-protected or corrupted
- Try a different PDF to isolate the issue

**Problem**: No text extracted from PDF
- **Solution**: PDF might be image-based (scanned document)
- Use OCR tools to convert to searchable PDF first

---

## 🎯 Use Cases

- 🎓 **Class 11 Physics Students**: Query the preloaded Halliday-Resnick-Walker textbook instantly (1,452 pages ready!)
- 📚 **Students**: Query textbooks, lecture notes, and study materials
- 🔬 **Researchers**: Analyze research papers and technical documents
- 💼 **Professionals**: Search through manuals, reports, and documentation
- 📖 **Readers**: Ask questions about books and articles
- 👨‍� **Educators**: Create interactive learning experiences

---

## 🚀 Future Enhancements

- [ ] Multi-document chat with document selection
- [ ] Conversation history and context
- [ ] Export answers to PDF/Markdown
- [ ] Support for multiple file formats (DOCX, TXT, etc.)
- [ ] Advanced search filters and options
- [ ] User authentication and document management
- [ ] Cloud deployment (Docker, AWS, Azure)
- [ ] Mobile app (React Native)

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the **MIT License** - feel free to use for personal or commercial projects!

---

## 🙏 Acknowledgments

- **Groq** for providing free, ultra-fast AI inference
- **Google** for the Gemini API
- **Sentence-Transformers** for excellent embedding models
- **ChromaDB** for the vector database
- **FastAPI** for the amazing web framework
- **React** and **Vite** for the frontend tools

---

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Troubleshooting](#-troubleshooting) section
2. Review the documentation files in the repository
3. Open an issue on GitHub

---

## ⭐ Star This Repository

If you find this project helpful, please consider giving it a star! ⭐

---

**Built with ❤️ using FastAPI, React, ChromaDB, and AI**
