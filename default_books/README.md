# Default Book - Halliday-Resnick-Walker Physics

## 📚 Currently Loaded Book

**Title**: Fundamentals of Physics  
**Authors**: Halliday, Resnick, Walker  
**Edition**: 11th Edition  
**Target**: Class 11 Physics Syllabus  
**Pages**: 1,452 pages  
**Size**: ~40 MB  
**Chunks**: 2,217 searchable chunks  

## ✅ Status

✓ **Book is already loaded and ready to use!**

The system automatically loads this book on startup. Thanks to the embedding cache optimization, subsequent server restarts take only ~5 seconds instead of ~2 minutes!

## 🎯 What You Can Ask

This textbook covers the complete Class 11 Physics syllabus. Example questions:

### Mechanics
- "What is Newton's second law of motion?"
- "Derive the equation for projectile motion"
- "Explain the concept of work and energy"
- "What is the law of conservation of momentum?"

### Thermodynamics
- "What are the laws of thermodynamics?"
- "Explain the concept of entropy"
- "What is the first law of thermodynamics?"

### Waves & Oscillations
- "What is simple harmonic motion?"
- "Explain the properties of waves"
- "What is the Doppler effect?"

### Electricity & Magnetism
- "What is Coulomb's law?"
- "Explain Ohm's law"
- "What is electromagnetic induction?"

## 🔄 Replacing the Default Book

If you want to replace this book with your own:

1. **Delete the current book**:
   ```bash
   rm default_books/default_book.pdf
   ```

2. **Add your new book**:
   - Place your PDF in this folder
   - Name it: `default_book.pdf`

3. **Clear the database** (to remove old embeddings):
   ```bash
   rm -rf backend/chroma_db
   ```
   Or use the API:
   ```bash
   curl -X DELETE http://localhost:8000/clear
   ```

4. **Restart the backend**:
   ```bash
   python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
   ```

The new book will be processed and cached automatically!

## 📊 Performance

- **First Load**: ~2 minutes (generates embeddings)
- **Subsequent Loads**: ~5 seconds (loads from cache)
- **Database Size**: ~15 MB (persistent storage)

## 📖 See Also

- [HOW_TO_ADD_DEFAULT_BOOK.md](../HOW_TO_ADD_DEFAULT_BOOK.md) - Detailed instructions
- [EMBEDDING_CACHE_OPTIMIZATION.md](../EMBEDDING_CACHE_OPTIMIZATION.md) - How caching works
- [README.md](../README.md) - Main documentation
