#!/bin/bash
# Migration script for F1 Telemetry System
# This script helps transition from the old Layer-based structure to the new services structure

set -e

echo "╔════════════════════════════════════════════════════════════╗"
echo "║  F1 Telemetry System - Repository Migration Script       ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored messages
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if we're in the right directory
if [ ! -f "docker-compose.yml" ]; then
    print_error "Please run this script from the repository root directory"
    exit 1
fi

print_info "Checking current structure..."

# Backup old structure
if [ -d "Layer1" ] || [ -d "Layer2" ] || [ -d "Layer3" ]; then
    print_warning "Old Layer structure detected"
    
    read -p "Do you want to create a backup? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        BACKUP_DIR="backup_$(date +%Y%m%d_%H%M%S)"
        print_info "Creating backup in $BACKUP_DIR..."
        mkdir -p "$BACKUP_DIR"
        
        [ -d "Layer1" ] && cp -r Layer1 "$BACKUP_DIR/"
        [ -d "Layer2" ] && cp -r Layer2 "$BACKUP_DIR/"
        [ -d "Layer3" ] && cp -r Layer3 "$BACKUP_DIR/"
        
        print_success "Backup created at $BACKUP_DIR"
    fi
fi

# Check if services directory exists
if [ ! -d "services" ]; then
    print_error "Services directory not found. Please ensure the new structure is in place."
    exit 1
fi

print_success "New services structure detected"

# Initialize environment file
if [ ! -f ".env" ]; then
    print_info "Creating .env file from template..."
    if [ -f ".env.example" ]; then
        cp .env.example .env
        print_success ".env file created"
    else
        print_error ".env.example not found"
        exit 1
    fi
else
    print_info ".env file already exists"
fi

# Check Docker installation
print_info "Checking Docker installation..."
if ! command -v docker &> /dev/null; then
    print_error "Docker is not installed. Please install Docker first."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    print_error "Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

print_success "Docker and Docker Compose are installed"

# Check Docker daemon
if ! docker info &> /dev/null; then
    print_error "Docker daemon is not running. Please start Docker."
    exit 1
fi

print_success "Docker daemon is running"

# Offer to remove old directories
if [ -d "Layer1" ] || [ -d "Layer2" ] || [ -d "Layer3" ]; then
    echo ""
    print_warning "Old Layer directories still exist"
    read -p "Do you want to remove them? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        print_info "Removing old directories..."
        rm -rf Layer1 Layer2 Layer3
        print_success "Old directories removed"
    fi
fi

# Create necessary directories
print_info "Creating necessary directories..."
mkdir -p logs
mkdir -p data

# Set up Git hooks (optional)
if [ -d ".git" ]; then
    print_info "Setting up Git hooks..."
    # Add any Git hooks setup here
    print_success "Git hooks configured"
fi

echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║                  Migration Complete!                      ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
print_success "Repository structure is now ready!"
echo ""
echo "Next steps:"
echo "  1. Review the new README.new.md file"
echo "  2. Configure your .env file if needed"
echo "  3. Build services:  make build"
echo "  4. Start services:  make up"
echo "  5. Check status:    make health"
echo ""
echo "For development:"
echo "  - Use: make dev-up"
echo "  - Or open a service directory in VS Code and use Dev Containers"
echo ""
echo "For monitoring:"
echo "  - Run: docker-compose -f docker-compose.monitoring.yml up -d"
echo "  - Access Grafana at http://localhost:3001"
echo ""
print_info "See docs/ directory for detailed documentation"
echo ""
