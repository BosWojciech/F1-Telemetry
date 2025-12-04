.PHONY: help build up down logs clean dev-up dev-down restart ps health

# Colors for output
BLUE := \033[0;34m
GREEN := \033[0;32m
RED := \033[0;31m
NC := \033[0m # No Color

help: ## Show this help message
	@echo "$(BLUE)F1 Telemetry System - Make Commands$(NC)"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(GREEN)%-20s$(NC) %s\n", $$1, $$2}'

# Production Commands
build: ## Build all services
	@echo "$(BLUE)Building all services...$(NC)"
	docker-compose build

up: ## Start all services in production mode
	@echo "$(BLUE)Starting all services in production mode...$(NC)"
	docker-compose up -d
	@echo "$(GREEN)Services started successfully!$(NC)"
	@echo "Frontend: http://localhost:3000"
	@echo "WebSocket: ws://localhost:8765"

down: ## Stop all services
	@echo "$(RED)Stopping all services...$(NC)"
	docker-compose down

# Development Commands
dev-build: ## Build all services for development
	@echo "$(BLUE)Building all services for development...$(NC)"
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml build

dev-up: ## Start all services in development mode with hot reload
	@echo "$(BLUE)Starting all services in development mode...$(NC)"
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d
	@echo "$(GREEN)Development services started!$(NC)"
	@echo "Frontend: http://localhost:5173"
	@echo "WebSocket: ws://localhost:8765"
	@echo "Python Debugger: localhost:5678"

dev-down: ## Stop development services
	@echo "$(RED)Stopping development services...$(NC)"
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml down

dev-logs: ## View development logs
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml logs -f

# Service-specific commands
logs: ## View logs from all services
	docker-compose logs -f

logs-ingest: ## View logs from telemetry-ingest service
	docker-compose logs -f telemetry-ingest

logs-processor: ## View logs from telemetry-processor service
	docker-compose logs -f telemetry-processor

logs-frontend: ## View logs from telemetry-frontend service
	docker-compose logs -f telemetry-frontend

# Utility commands
ps: ## List running services
	docker-compose ps

health: ## Check health status of all services
	@echo "$(BLUE)Service Health Status:$(NC)"
	@docker-compose ps --format "table {{.Service}}\t{{.Status}}\t{{.Health}}"

restart: ## Restart all services
	@echo "$(BLUE)Restarting all services...$(NC)"
	docker-compose restart

restart-ingest: ## Restart telemetry-ingest service
	docker-compose restart telemetry-ingest

restart-processor: ## Restart telemetry-processor service
	docker-compose restart telemetry-processor

restart-frontend: ## Restart telemetry-frontend service
	docker-compose restart telemetry-frontend

# Shell access
shell-ingest: ## Open shell in telemetry-ingest container
	docker-compose exec telemetry-ingest /bin/bash

shell-processor: ## Open shell in telemetry-processor container
	docker-compose exec telemetry-processor /bin/bash

shell-frontend: ## Open shell in telemetry-frontend container
	docker-compose exec telemetry-frontend /bin/sh

# Cleanup commands
clean: ## Remove all containers, volumes, and images
	@echo "$(RED)Cleaning up all resources...$(NC)"
	docker-compose down -v --rmi all
	@echo "$(GREEN)Cleanup complete!$(NC)"

clean-volumes: ## Remove all volumes (WARNING: deletes data)
	@echo "$(RED)Removing all volumes...$(NC)"
	docker-compose down -v
	@echo "$(GREEN)Volumes removed!$(NC)"

prune: ## Remove unused Docker resources
	@echo "$(RED)Pruning unused Docker resources...$(NC)"
	docker system prune -af --volumes
	@echo "$(GREEN)Prune complete!$(NC)"

# Testing commands
test: ## Run tests for all services
	@echo "$(BLUE)Running tests...$(NC)"
	docker-compose exec telemetry-processor pytest
	@echo "$(GREEN)Tests complete!$(NC)"

# Initialization
init: ## Initialize the project (copy .env.example to .env)
	@if [ ! -f .env ]; then \
		cp .env.example .env; \
		echo "$(GREEN).env file created from .env.example$(NC)"; \
	else \
		echo "$(RED).env file already exists$(NC)"; \
	fi

# Quick start
quickstart: init build up ## Initialize, build, and start all services
	@echo "$(GREEN)F1 Telemetry System is ready!$(NC)"
	@echo "Access the dashboard at: http://localhost:3000"

dev-quickstart: init dev-build dev-up ## Initialize, build, and start in dev mode
	@echo "$(GREEN)F1 Telemetry Development Environment is ready!$(NC)"
	@echo "Access the dashboard at: http://localhost:5173"
