# -------------------------------
# Frontend build stage
# -------------------------------
FROM node:20 AS frontend-build

WORKDIR /app/frontend

# Copy package.json and package-lock.json
COPY frontend/package*.json ./

# Install dependencies (ci if lockfile exists, otherwise install)
RUN npm ci || npm install

# Copy rest of frontend code
COPY frontend/ ./

# Build production frontend
RUN npm run build


# -------------------------------
# Backend stage
# -------------------------------
FROM python:3.11-slim AS backend

WORKDIR /app

# Install system dependencies (for numpy, torch, etc.)
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python deps
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend source code
COPY backend/ ./backend

# Copy built frontend from frontend-build
COPY --from=frontend-build /app/frontend/dist ./frontend_dist

# Expose backend port
EXPOSE 8000

# Start FastAPI backend with Uvicorn
CMD ["uvicorn", "backend.app:app", "--host", "0.0.0.0", "--port", "8000"]
