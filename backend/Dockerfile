FROM python:3.12-slim

WORKDIR /app

# Install system dependency for XGBoost on Linux (no libomp needed on Linux)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code and pre-trained model
COPY backend/ .

# Expose port (Railway sets $PORT automatically)
EXPOSE 8000

# Start server
CMD uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}
