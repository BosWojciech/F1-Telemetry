# Multi-stage build for React Telemetry Frontend

# ============================================
# Stage 1: Dependencies Stage
# ============================================
FROM node:20-alpine AS dependencies

WORKDIR /app

# Copy package files
COPY package.json package-lock.json* ./

# Install dependencies
RUN npm ci

# ============================================
# Stage 2: Builder Stage
# ============================================
FROM node:20-alpine AS builder

WORKDIR /app

# Copy dependencies from dependencies stage
COPY --from=dependencies /app/node_modules ./node_modules

# Copy source code
COPY . .

# Build the application
RUN npm run build

# ============================================
# Stage 3: Development Stage
# ============================================
FROM node:20-alpine AS development

WORKDIR /app

# Install development tools
RUN apk add --no-cache git curl

# Copy dependencies from dependencies stage
COPY --from=dependencies /app/node_modules ./node_modules

# Copy source code
COPY . .

# Create non-root user
RUN addgroup -g 1000 telemetry && \
    adduser -D -u 1000 -G telemetry telemetry && \
    chown -R telemetry:telemetry /app

USER telemetry

EXPOSE 5173

CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]

# ============================================
# Stage 4: Runtime Stage (Production with Nginx)
# ============================================
FROM nginx:alpine AS runtime

# Copy built assets from builder stage
COPY --from=builder /app/dist /usr/share/nginx/html

# Copy custom Nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Create non-root user for Nginx
RUN addgroup -g 1000 telemetry && \
    adduser -D -u 1000 -G telemetry telemetry && \
    chown -R telemetry:telemetry /usr/share/nginx/html && \
    chown -R telemetry:telemetry /var/cache/nginx && \
    chown -R telemetry:telemetry /var/log/nginx && \
    touch /var/run/nginx.pid && \
    chown -R telemetry:telemetry /var/run/nginx.pid

USER telemetry

EXPOSE 80

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=20s --retries=3 \
    CMD wget --quiet --tries=1 --spider http://localhost:80 || exit 1

CMD ["nginx", "-g", "daemon off;"]
