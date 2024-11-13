# Frontend Dockerfile (Vite/Node)
FROM node:18 AS builder
WORKDIR /app

# Copy package.json and install dependencies
COPY package.json ./ 
RUN npm install

# Copy the rest of the frontend source code
COPY . ./ 

# Build the frontend using Vite
RUN npm run build

# Production stage
FROM node:18-slim AS production
WORKDIR /app

# Copy built assets from builder stage
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/package.json ./

# Install only production dependencies
RUN npm install --production

# Expose frontend port
EXPOSE 3000

# Start the frontend server
CMD ["node", "run", "preview"]