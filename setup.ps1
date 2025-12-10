# AI PDF Q&A Setup Script

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  AI PDF Q&A System - Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check Python
Write-Host "Checking Python installation..." -ForegroundColor Yellow
python --version
if ($LASTEXITCODE -ne 0) {
    Write-Host "Error: Python not found. Please install Python 3.9+" -ForegroundColor Red
    exit 1
}

# Check Node.js
Write-Host "Checking Node.js installation..." -ForegroundColor Yellow
node --version
if ($LASTEXITCODE -ne 0) {
    Write-Host "Error: Node.js not found. Please install Node.js 16+" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Step 1: Setting up Python virtual environment..." -ForegroundColor Green
python -m venv venv

Write-Host ""
Write-Host "Step 2: Activating virtual environment..." -ForegroundColor Green
.\venv\Scripts\Activate.ps1

Write-Host ""
Write-Host "Step 3: Installing Python dependencies..." -ForegroundColor Green
pip install -r requirements.txt

Write-Host ""
Write-Host "Step 4: Installing frontend dependencies..." -ForegroundColor Green
Set-Location frontend
npm install
Set-Location ..

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Setup Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next Steps:" -ForegroundColor Yellow
Write-Host "1. Add your Gemini API key to .env file" -ForegroundColor White
Write-Host "   Get one at: https://makersuite.google.com/app/apikey" -ForegroundColor White
Write-Host ""
Write-Host "2. Start the backend (Terminal 1):" -ForegroundColor White
Write-Host "   .\venv\Scripts\activate" -ForegroundColor Cyan
Write-Host "   uvicorn backend.main:app --reload" -ForegroundColor Cyan
Write-Host ""
Write-Host "3. Start the frontend (Terminal 2):" -ForegroundColor White
Write-Host "   cd frontend" -ForegroundColor Cyan
Write-Host "   npm run dev" -ForegroundColor Cyan
Write-Host ""
