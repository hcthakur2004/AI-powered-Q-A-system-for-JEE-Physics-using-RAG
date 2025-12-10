import { useState, useEffect } from 'react';
import './index.css';

const API_URL = 'http://localhost:8000';

function App() {
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [currentView, setCurrentView] = useState('home');
  const [darkMode, setDarkMode] = useState(() => {
    // Check localStorage or system preference
    const saved = localStorage.getItem('darkMode');
    if (saved !== null) {
      return JSON.parse(saved);
    }
    return window.matchMedia('(prefers-color-scheme: dark)').matches;
  });
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [uploadStatus, setUploadStatus] = useState(null);
  const [question, setQuestion] = useState('');
  const [asking, setAsking] = useState(false);
  const [answer, setAnswer] = useState(null);
  const [dragging, setDragging] = useState(false);
  const [bookStatus, setBookStatus] = useState(null);

  // Apply dark mode
  useEffect(() => {
    if (darkMode) {
      document.documentElement.setAttribute('data-theme', 'dark');
    } else {
      document.documentElement.removeAttribute('data-theme');
    }
    localStorage.setItem('darkMode', JSON.stringify(darkMode));
  }, [darkMode]);

  // Fetch book status on mount
  useEffect(() => {
    const fetchBookStatus = async () => {
      try {
        const response = await fetch(`${API_URL}/book-status`);
        const data = await response.json();
        setBookStatus(data);
      } catch (error) {
        console.error('Failed to fetch book status:', error);
      }
    };
    fetchBookStatus();
  }, []);

  const toggleDarkMode = () => {
    setDarkMode(!darkMode);
  };



  // Handle file selection
  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile && selectedFile.type === 'application/pdf') {
      setFile(selectedFile);
      setUploadStatus(null);
      setAnswer(null);
    } else {
      setUploadStatus({
        type: 'error',
        message: 'Please select a valid PDF file'
      });
    }
  };

  // Handle drag and drop
  const handleDragOver = (e) => {
    e.preventDefault();
    setDragging(true);
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    setDragging(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setDragging(false);

    const droppedFile = e.dataTransfer.files[0];
    if (droppedFile && droppedFile.type === 'application/pdf') {
      setFile(droppedFile);
      setUploadStatus(null);
      setAnswer(null);
    } else {
      setUploadStatus({
        type: 'error',
        message: 'Please drop a valid PDF file'
      });
    }
  };

  // Upload PDF
  const handleUpload = async () => {
    if (!file) {
      setUploadStatus({
        type: 'error',
        message: 'Please select a PDF file first'
      });
      return;
    }

    setUploading(true);
    setUploadStatus(null);
    setAnswer(null);

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch(`${API_URL}/upload`, {
        method: 'POST',
        body: formData,
      });

      const data = await response.json();

      if (response.ok) {
        setUploadStatus({
          type: 'success',
          message: `✓ ${data.filename} processed successfully! ${data.pages} pages, ${data.chunks} chunks created.`
        });

        // Refresh book status
        try {
          const statusResponse = await fetch(`${API_URL}/book-status`);
          const statusData = await statusResponse.json();
          setBookStatus(statusData);
        } catch (error) {
          console.error('Failed to refresh book status:', error);
        }
      } else {
        setUploadStatus({
          type: 'error',
          message: data.detail || 'Upload failed'
        });
      }
    } catch (error) {
      setUploadStatus({
        type: 'error',
        message: 'Failed to connect to server. Make sure the backend is running.'
      });
    } finally {
      setUploading(false);
    }
  };

  // Ask question
  const handleAskQuestion = async (e) => {
    e.preventDefault();

    if (!question.trim()) {
      return;
    }

    setAsking(true);
    setAnswer(null);

    try {
      const response = await fetch(`${API_URL}/ask`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ question: question.trim() }),
      });

      const data = await response.json();

      if (response.ok) {
        setAnswer(data);
      } else {
        setAnswer({
          question: question,
          answer: `Error: ${data.detail}`,
          sources: []
        });
      }
    } catch (error) {
      setAnswer({
        question: question,
        answer: 'Failed to get answer. Make sure the backend is running and a PDF is uploaded.',
        sources: []
      });
    } finally {
      setAsking(false);
    }
  };

  const renderHome = () => (
    <>
      <div className="page-header">
        <h1 className="page-title">Welcome to JEE Phy AI</h1>
        <p className="page-subtitle">AI-powered tools for JEE Physics preparation and learning</p>
      </div>

      {/* Default Book Status */}
      {bookStatus && bookStatus.has_default_book && (
        <div className="content-card" style={{
          background: 'linear-gradient(135deg, rgba(124, 58, 237, 0.1), rgba(37, 99, 235, 0.1))',
          borderLeft: '4px solid var(--color-brand-blue)',
          marginBottom: 'var(--spacing-lg)'
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--spacing-md)', marginBottom: 'var(--spacing-sm)' }}>
            <span style={{ fontSize: '2rem' }}>📖</span>
            <div>
              <h3 style={{ marginBottom: '0.25rem', color: 'var(--color-brand-blue)' }}>Default Book Loaded</h3>
              <p style={{ color: 'var(--text-secondary)', margin: 0, fontWeight: '500' }}>
                Halliday–Resnick–Walker, Fundamentals of Physics, 11th Edition
              </p>
              <p style={{ color: 'var(--text-tertiary)', margin: 0, fontSize: '0.875rem' }}>
                Class 11 syllabus • {bookStatus.total_chunks} chunks available
              </p>
            </div>
          </div>
          <p style={{ color: 'var(--text-secondary)', marginBottom: 'var(--spacing-md)', fontSize: '0.9rem' }}>
            You can start asking questions immediately from the pre-loaded book, or upload additional PDFs to expand the knowledge base.
          </p>
          <button
            className="btn btn-primary"
            onClick={() => setCurrentView('ask')}
          >
            💬 Start Asking Questions
          </button>
        </div>
      )}

      {/* No Default Book Message */}
      {bookStatus && !bookStatus.has_default_book && !bookStatus.documents_loaded && (
        <div className="content-card" style={{
          background: 'rgba(251, 146, 60, 0.1)',
          borderLeft: '4px solid var(--color-orange)',
          marginBottom: 'var(--spacing-lg)'
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--spacing-md)' }}>
            <span style={{ fontSize: '2rem' }}>ℹ️</span>
            <div>
              <h3 style={{ marginBottom: '0.25rem', color: 'var(--color-orange)' }}>No Book Loaded</h3>
              <p style={{ color: 'var(--text-secondary)', margin: 0 }}>
                Upload a PDF to get started with AI-powered question answering
              </p>
            </div>
          </div>
        </div>
      )}

      <div className="feature-grid">

        <button
          className="feature-card purple"
          onClick={() => setCurrentView('upload')}
        >
          <div className="feature-icon">📚</div>
          <h3 className="feature-title">Upload PDF</h3>
        </button>

        <button
          className="feature-card blue"
          onClick={() => setCurrentView('ask')}
        >
          <div className="feature-icon">💬</div>
          <h3 className="feature-title">Ask Questions</h3>
        </button>


      </div>

      <div className="content-card">
        <h3>🎯 How It Works</h3>
        <p style={{ color: 'var(--text-secondary)', lineHeight: '1.8' }}>
          This system uses <strong>Retrieval Augmented Generation (RAG)</strong> with embeddings.
          Your PDF is split into chunks, converted to vector embeddings using sentence-transformers,
          and stored in ChromaDB. When you ask a question, we find the most relevant chunks and
          use Gemini AI to generate accurate answers based on your document's content.
        </p>
      </div>
    </>
  );

  const renderUpload = () => (
    <>
      <button className="back-btn" onClick={() => setCurrentView('home')}>
        ← Back
      </button>

      <div className="page-header">
        <h1 className="page-title">Upload PDF</h1>
        <p className="page-subtitle">Upload your JEE Physics study material to get started</p>
      </div>

      <div className="content-card">
        <div
          className={`upload-zone ${dragging ? 'dragging' : ''}`}
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
          onClick={() => document.getElementById('file-input').click()}
        >
          <div className="upload-icon">📄</div>
          <h3>{file ? file.name : 'Upload Your PDF'}</h3>
          <p>
            {file
              ? `File selected: ${(file.size / 1024 / 1024).toFixed(2)} MB`
              : 'Drag and drop or click to browse'
            }
          </p>
          <input
            id="file-input"
            type="file"
            accept=".pdf"
            onChange={handleFileChange}
          />
          <button
            className="btn btn-primary"
            onClick={(e) => {
              e.stopPropagation();
              handleUpload();
            }}
            disabled={!file || uploading}
          >
            {uploading ? (
              <>
                <span className="spinner"></span> Processing...
              </>
            ) : (
              '🚀 Upload & Process'
            )}
          </button>
        </div>

        {uploadStatus && (
          <div className={`status-message ${uploadStatus.type}`}>
            <span>{uploadStatus.message}</span>
          </div>
        )}
      </div>

      {uploadStatus?.type === 'success' && (
        <div className="content-card">
          <h3>✅ PDF Processed Successfully!</h3>
          <p style={{ color: 'var(--text-secondary)', marginBottom: 'var(--spacing-md)' }}>
            Your document has been processed and is ready for questions.
          </p>
          <button
            className="btn btn-primary"
            onClick={() => setCurrentView('ask')}
          >
            💬 Start Asking Questions
          </button>
        </div>
      )}
    </>
  );

  const renderAsk = () => (
    <>
      <button className="back-btn" onClick={() => setCurrentView('home')}>
        ← Back
      </button>

      <div className="page-header">
        <h1 className="page-title">Ask Questions</h1>
        <p className="page-subtitle">Get AI-powered answers from your uploaded documents</p>
      </div>

      <div className="content-card">
        <h2>💬 Ask a Question</h2>
        <form onSubmit={handleAskQuestion} className="question-form">
          <div className="input-wrapper">
            <input
              type="text"
              className="question-input"
              placeholder="What would you like to know about this document?"
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              disabled={asking}
            />
          </div>
          <button
            type="submit"
            className="btn btn-primary"
            disabled={!question.trim() || asking}
          >
            {asking ? (
              <>
                <span className="spinner"></span> Thinking...
              </>
            ) : (
              '🔍 Ask'
            )}
          </button>
        </form>

        {/* Answer Display */}
        {answer && (
          <div className="answer-container">
            <h3 style={{ marginBottom: 'var(--spacing-md)', color: 'var(--color-brand-blue)' }}>
              💡 Answer
            </h3>

            <div style={{
              background: 'var(--bg-primary)',
              padding: 'var(--spacing-lg)',
              borderRadius: 'var(--radius-md)',
              marginBottom: 'var(--spacing-lg)'
            }}>
              <p className="answer-text">{answer.answer}</p>
            </div>

            {/* Sources */}
            {answer.sources && answer.sources.length > 0 && (
              <div className="sources-section">
                <h4 className="sources-header">📚 Sources from Document</h4>
                <div className="sources-list">
                  {answer.sources.map((source, index) => (
                    <div key={index} className="source-item">
                      <div className="source-meta">
                        <span>📄 Page {source.page + 1}</span>
                        <span>•</span>
                        <span>Chunk #{source.chunk_id}</span>
                      </div>
                      <p className="source-text">{source.text}</p>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </>
  );

  return (
    <div className="app">
      {/* Header */}
      <header className="header">
        <div className="header-left">
          <button className="menu-btn" onClick={() => setSidebarOpen(!sidebarOpen)}>
            ☰
          </button>
          <a href="#" className="logo" onClick={(e) => { e.preventDefault(); setCurrentView('home'); }}>
            <span className="logo-icon">🧠</span>
            <span>JEE Phy AI</span>
          </a>
        </div>
        <div className="header-right">
          <div className="header-icons">
            <button className="icon-btn" onClick={toggleDarkMode} title={darkMode ? 'Switch to Light Mode' : 'Switch to Dark Mode'}>
              {darkMode ? '☀️' : '🌙'}
            </button>
          </div>
          <div className="user-info">
            <span>Student</span>
          </div>
        </div>
      </header>

      {/* Sidebar */}
      <aside className={`sidebar ${sidebarOpen ? 'open' : 'closed'}`}>
        <nav className="sidebar-nav">
          <button
            className={`nav-item ${currentView === 'home' ? 'active' : ''}`}
            onClick={() => setCurrentView('home')}
          >
            <span className="nav-icon">🏠</span>
            <span>Home</span>
          </button>
          <button
            className={`nav-item ${currentView === 'upload' ? 'active' : ''}`}
            onClick={() => setCurrentView('upload')}
          >
            <span className="nav-icon">📚</span>
            <span>Upload PDF</span>
          </button>
          <button
            className={`nav-item ${currentView === 'ask' ? 'active' : ''}`}
            onClick={() => setCurrentView('ask')}
          >
            <span className="nav-icon">💬</span>
            <span>Ask Questions</span>
          </button>

        </nav>

        <div className="sidebar-footer">
          <button className="sign-out-btn">
            <span className="nav-icon">🚪</span>
            <span>Sign Out</span>
          </button>
        </div>
      </aside>

      {/* Main Content */}
      <main className={`main-content ${sidebarOpen ? '' : 'sidebar-closed'}`}>
        {currentView === 'home' && renderHome()}
        {currentView === 'upload' && renderUpload()}
        {currentView === 'ask' && renderAsk()}
      </main>
    </div>
  );
}

export default App;
