# Build stage
FROM node:20-alpine AS build

WORKDIR /app

# Set working directory
ENV PYTHONPATH=/app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci

# Copy application code
COPY . .

# Build application
RUN npm run build

# Development stage
FROM node:20-alpine AS dev

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy application code
COPY . .

# Expose Vite default port (configured to 4200 in vite.config.ts)
EXPOSE 4200

# Start dev server
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]

