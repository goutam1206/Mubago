# ================================
# 1. Base image
# ================================
FROM python:3.12-slim AS builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install dependencies first (cached)
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy app code
COPY . .

# ================================
# 2. Final minimal image
# ================================
FROM python:3.12-slim

WORKDIR /app

# Copy from builder
COPY --from=builder /usr/local /usr/local
COPY --from=builder /app /app

# Environment variables
ENV PYTHONUNBUFFERED=1 \
    PORT=8000

EXPOSE 8000

# Health check (optional)
HEALTHCHECK CMD curl --fail http://localhost:8000/health || exit 1

# Run FastAPI via Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]