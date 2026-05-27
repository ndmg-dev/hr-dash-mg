# Stage 1: Build Frontend
FROM node:20-alpine AS frontend-builder
WORKDIR /app/frontend

COPY frontend/package*.json ./
RUN npm ci

COPY frontend/ ./
RUN npm run build

# Stage 2: Setup Backend and Serve
FROM python:3.12-slim
WORKDIR /app

# Install system dependencies (for pandas if needed)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend application
COPY backend/app ./app
COPY backend/data ./data

# Copy built frontend assets
COPY --from=frontend-builder /app/frontend/dist ./static

# Configure environment variables
ENV HR_ENVIRONMENT=production
ENV PYTHONUNBUFFERED=1

# Expose the API port
EXPOSE 8000

# Start Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
