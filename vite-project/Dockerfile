# === Multi-Stage Dockerfile ===

# --- Stage 1: Frontend Build (Vite) ---
FROM node:18 AS frontend-build
WORKDIR /app/frontend

# Copy frontend package.json and install dependencies
COPY frontend/package.json ./ 
RUN npm install

# Copy the rest of the frontend source code
COPY frontend/ ./ 

# Build the frontend using Vite
RUN npm run build

# --- Stage 2: Backend Build ---
FROM python:3.11-slim as backend-build
WORKDIR /app/backend

# Install build dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev

# Copy Flask requirements and install dependencies
COPY backend/requirements.txt ./ 
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the Flask source code
COPY backend/ ./

# --- Final Stage: Combined Runtime ---
FROM python:3.11-slim
WORKDIR /app

# Install Node.js
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    curl \
    gnupg && \
    curl -fsSL https://deb.nodesource.com/setup_18.x | bash - && \
    apt-get install -y nodejs && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy Frontend Build Output
COPY --from=frontend-build /app/frontend/dist /app/frontend/dist

# Copy Backend and its dependencies
COPY --from=backend-build /app/backend /app/backend
COPY --from=backend-build /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=backend-build /usr/local/bin /usr/local/bin

# Expose necessary ports
EXPOSE 3000 5000

# Command to start both the frontend (Vite/Node) and backend (Flask)
CMD ["sh", "-c", "node /app/frontend/dist/server.js & python3 /app/backend/main.py"]