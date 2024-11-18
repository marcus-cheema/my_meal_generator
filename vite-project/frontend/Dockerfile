# Frontend Dockerfile (Vite/Node)
FROM node:18-alpine AS builder
WORKDIR /app

# Copy package.json and package-lock.json
COPY package.json package-lock.json ./ 
RUN npm install

COPY . .

# Build the frontend w/ Vite
RUN npm run build

# Production stage
FROM nginx:alpine AS production
WORKDIR /usr/share/nginx/html

# Copy built assets from builder stage
COPY --from=builder /app/dist . 

# Expose Port (nginx default)
EXPOSE 80

# Run the server
CMD ["nginx", "-g", "daemon off;"]
