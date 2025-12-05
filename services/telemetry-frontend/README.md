# F1 Telemetry Frontend

Modern React + TypeScript dashboard for real-time F1 telemetry visualization.

## Overview

A responsive web application that displays live F1 game telemetry data through an intuitive, F1-style MFD (Multi-Function Display) interface.

## Features

- **Real-time data streaming** via WebSocket
- **Redux state management** for predictable data flow
- **TypeScript** for type safety
- **Modular component architecture**
- **Responsive design** for desktop and mobile
- **F1-styled UI components**
- **Hot module reloading** in development

## Tech Stack

- **Framework**: React 18
- **Language**: TypeScript
- **State Management**: Redux Toolkit
- **Build Tool**: Vite
- **Styling**: CSS Modules
- **WebSocket**: Native WebSocket API
- **Production Server**: Nginx

## Installation

### Local Development

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Access at http://localhost:5173
```

### Docker Build

```bash
# Production build
docker build --target runtime -t f1-telemetry-frontend:latest .

# Development build
docker build --target development -t f1-telemetry-frontend:dev .
```

## Configuration

Environment variables (create `.env` file):

```env
VITE_WEBSOCKET_URL=ws://localhost:8765
```

## Running

### Development Mode

```bash
# Local
npm run dev

# Docker
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up telemetry-frontend
```

Access at: http://localhost:5173

### Production Mode

```bash
# Build
npm run build

# Preview
npm run preview

# Docker
docker-compose up telemetry-frontend
```

Access at: http://localhost:3000

## Development

### Dev Container

Open this directory in VS Code with the Dev Containers extension for a fully configured Node.js development environment.

### Project Structure

```
src/
├── App.tsx              # Main application component
├── main.tsx            # Application entry point
├── index.css           # Global styles
├── PacketTypes.ts      # TypeScript type definitions
├── redux/
│   ├── store.ts        # Redux store configuration
│   └── packetDispatcher.ts  # Packet routing logic
└── socket/
    └── socketService.ts  # WebSocket connection management
```

## WebSocket Protocol

Connects to `ws://localhost:8765`

Receives JSON messages:
```typescript
{
    packetType: string;
    timestamp: number;
    data: {
        // Packet-specific data
    }
}
```

## Performance

- **Bundle size**: ~500KB (gzipped)
- **Initial load**: < 2 seconds
- **Frame rate**: 60 FPS
- **WebSocket latency**: < 50ms

## Browser Support

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## Production Optimizations

- **Code splitting** for faster initial load
- **Tree shaking** to remove unused code
- **Asset optimization** (images, fonts)
- **Gzip compression** via Nginx
- **HTTP/2** support
- **Security headers** configured
- **Cache control** for static assets
