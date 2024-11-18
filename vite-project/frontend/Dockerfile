# Frontend Dockerfile (Vite/Node)
FROM node:18-alpine AS builder
WORKDIR /app

# Copy package.json and package-lock.json
COPY package.json package-lock.json ./ 
RUN npm install

COPY . .
RUN npm run build

# Production

FROM node:18-alpine
WORKDIR /app

COPY --from=builder /app/dist ./dist

EXPOSE 3000

CMD ["npx", "serve", "-s", "dist", "-l", "3000"]
