# KubeRevive Production Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code
COPY . .

# Set PYTHONPATH
ENV PYTHONPATH=/app

EXPOSE 8000

# Health check probe
HEALTHCHECK --interval=15s --timeout=3s --retries=3 \
  CMD curl -f http://localhost:8000/api/status || exit 1

# Start FastAPI server
CMD ["uvicorn", "kuberevive.dashboard.app:app", "--host", "0.0.0.0", "--port", "8000"]

