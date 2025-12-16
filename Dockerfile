FROM python:3.9-slim

WORKDIR /app

# Install Node.js
RUN apt-get update && apt-get install -y nodejs npm && rm -rf /var/lib/apt/lists/*

# Copy all files
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Build frontend
WORKDIR /app/frontend
RUN npm install --legacy-peer-deps && npm run build

WORKDIR /app

# Expose port
EXPOSE 8000

# Start the backend server
CMD ["python", "-m", "uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
