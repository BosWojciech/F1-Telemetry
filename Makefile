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
	@echo "Telemetry Dashboard: http://localhost:3000"
	@echo "Simulator Frontend:  http://localhost:3001"
	@echo "WebSocket:           ws://localhost:8765"

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
	@echo "Telemetry Dashboard: http://localhost:5173"
	@echo "Simulator Frontend:  http://localhost:5174"
	@echo "WebSocket:           ws://localhost:8765"
	@echo "Python Debugger:     localhost:5678"

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

logs-simulator-backend: ## View logs from telemetry-simulator-backend service
	docker-compose logs -f telemetry-simulator-backend

logs-simulator-frontend: ## View logs from telemetry-simulator-frontend service
	docker-compose logs -f telemetry-simulator-frontend

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

restart-frontend: ## Restart telemetry-frontend service
	docker-compose restart telemetry-frontend

restart-simulator-backend: ## Restart telemetry-simulator-backend service
	docker-compose restart telemetry-simulator-backend

restart-simulator-frontend: ## Restart telemetry-simulator-frontend service
	docker-compose restart telemetry-simulator-frontend

restart-simulator: ## Restart telemetry-simulator service
	docker-compose restart telemetry-simulator

# Shell access
shell-ingest: ## Open shell in telemetry-ingest container
	docker-compose exec telemetry-ingest /bin/bash

shell-frontend: ## Open shell in telemetry-frontend container
	docker-compose exec telemetry-frontend /bin/sh

shell-simulator-backend: ## Open shell in telemetry-simulator-backend container
	docker-compose exec telemetry-simulator-backend /bin/sh

shell-simulator-frontend: ## Open shell in telemetry-simulator-frontend container
	docker-compose exec telemetry-simulator-frontend /bin/sh

# Protobuf
F1_GAME_VERSION ?= 23
PROTO_SRC_DIR := proto/f1_$(F1_GAME_VERSION)
SIMULATOR_BACKEND_PROTO_DIR := services/telemetry-simulator-backend/proto
SIMULATOR_FRONTEND_PROTO_DIR := services/telemetry-simulator-frontend/src/proto

.PHONY: setup-proto proto proto-backend proto-frontend

setup-proto: ## Check if protoc is installed
	@echo "$(BLUE)Checking for protoc installation...$(NC)"
	@which protoc > /dev/null 2>&1 || \
		(echo "$(RED)Error: protoc is not installed!$(NC)" && \
		 echo "$(BLUE)Please install Protocol Buffers compiler:$(NC)" && \
		 echo "  Visit: https://grpc.io/docs/protoc-installation/" && \
		 echo "" && \
		 echo "$(BLUE)Quick install options:$(NC)" && \
		 echo "  macOS:   brew install protobuf" && \
		 echo "  Linux:   apt install -y protobuf-compiler" && \
		 echo "  Windows: Download from https://github.com/protocolbuffers/protobuf/releases" && \
		 exit 1)
	@echo "$(GREEN)protoc found: $$(protoc --version)$(NC)"

proto: proto-backend proto-frontend ## Generate all protobuf files

proto-backend: setup-proto ## Generate protobuf files for simulator backend
proto: setup-proto ## Generate all protobuf files
	@echo "$(BLUE)Generating protobuf files for F1 $(F1_GAME_VERSION)...$(NC)"
	@echo ""
	@$(MAKE) proto-backend
	@echo ""
	@$(MAKE) proto-frontend
	@echo ""
	@echo "$(GREEN)✅ All protobuf files generated!$(NC)"

proto-backend: setup-proto ## Generate protobuf files for simulator backend
	@echo "$(BLUE)→ Generating Python protobuf files for simulator backend...$(NC)"
	@mkdir -p $(SIMULATOR_BACKEND_PROTO_DIR)
	@touch $(SIMULATOR_BACKEND_PROTO_DIR)/__init__.py
	protoc -I$(PROTO_SRC_DIR) --python_out=$(SIMULATOR_BACKEND_PROTO_DIR) --pyi_out=$(SIMULATOR_BACKEND_PROTO_DIR) $(PROTO_SRC_DIR)/enums.proto
	protoc -I$(PROTO_SRC_DIR) --python_out=$(SIMULATOR_BACKEND_PROTO_DIR) --pyi_out=$(SIMULATOR_BACKEND_PROTO_DIR) $(PROTO_SRC_DIR)/packet_definitions.proto
	@echo "$(GREEN)  ✓ Backend protobuf files generated in $(SIMULATOR_BACKEND_PROTO_DIR)$(NC)"

proto-frontend: setup-proto ## Generate protobuf files for simulator frontend (using ts-proto)
	@echo "$(BLUE)→ Generating TypeScript protobuf files for simulator frontend...$(NC)"
	@mkdir -p $(SIMULATOR_FRONTEND_PROTO_DIR)
	@cd services/telemetry-simulator-frontend && \
		if [ -d "node_modules" ]; then \
			npx protoc --plugin=./node_modules/.bin/protoc-gen-ts_proto --ts_proto_out=./src/proto \
				--ts_proto_opt=esModuleInterop=true \
				--ts_proto_opt=outputClientImpl=false \
				-I../../$(PROTO_SRC_DIR) \
				../../$(PROTO_SRC_DIR)/enums.proto \
				../../$(PROTO_SRC_DIR)/packet_definitions.proto 2>/dev/null || \
				(echo "$(RED)  ✗ ts-proto not installed. Install with: cd services/telemetry-simulator-frontend && npm install ts-proto$(NC)" && \
				 echo "$(BLUE)    Skipping frontend proto generation...$(NC)"); \
		else \
			echo "$(RED)  ✗ node_modules not found. Run: cd services/telemetry-simulator-frontend && npm install$(NC)"; \
			echo "$(BLUE)    Skipping frontend proto generation...$(NC)"; \
		fi
	@echo "$(GREEN)  ✓ Frontend protobuf generation completed$(NC)"
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
test: test-all ## Run all tests (alias for test-all)

test-all: test-cpp test-processor test-simulator test-frontend ## Run all unit tests
	@echo ""
	@echo "$(GREEN)═══════════════════════════════════════════════════════$(NC)"
	@echo "$(GREEN)✅ ALL UNIT TESTS COMPLETED$(NC)"
	@echo "$(GREEN)═══════════════════════════════════════════════════════$(NC)"
	@echo ""
	@echo "Run 'make test-e2e' to test the full pipeline"

test-cpp: ## Run C++ telemetry-ingest tests
	@echo ""
	@echo "$(BLUE)═══════════════════════════════════════════════════════$(NC)"
	@echo "$(BLUE)🔧 Running C++ Tests (telemetry-ingest)$(NC)"
	@echo "$(BLUE)═══════════════════════════════════════════════════════$(NC)"
	@echo ""
	@cd services/telemetry-ingest && \
		if [ ! -d "build" ]; then \
			echo "Building C++ project..."; \
			cmake --preset=default -DBUILD_TESTS=ON; \
		fi && \
		cmake --build build -j$$(nproc 2>/dev/null || sysctl -n hw.ncpu 2>/dev/null || echo 4) && \
		cd build && \
		ctest --output-on-failure --verbose
	@echo ""
	@echo "$(GREEN)✅ C++ tests passed!$(NC)"

test-processor: ## Run Python telemetry-processor tests
	@echo ""
	@echo "$(BLUE)═══════════════════════════════════════════════════════$(NC)"
	@echo "$(BLUE)🐍 Running Python Tests (telemetry-processor)$(NC)"
	@echo "$(BLUE)═══════════════════════════════════════════════════════$(NC)"
test-simulator: ## Run Python telemetry-simulator-backend tests
	@echo ""
	@echo "$(BLUE)═══════════════════════════════════════════════════════$(NC)"
	@echo "$(BLUE)🐍 Running Python Tests (telemetry-simulator-backend)$(NC)"
	@echo "$(BLUE)═══════════════════════════════════════════════════════$(NC)"
	@echo ""
	@cd services/telemetry-simulator-backend && \
		pytest tests/ -v --cov=. --cov-report=term-missing --cov-fail-under=50
	@echo ""
	@echo "$(GREEN)✅ Simulator tests passed!$(NC)"ry-simulator)$(NC)"
	@echo "$(BLUE)═══════════════════════════════════════════════════════$(NC)"
	@echo ""
	@cd services/telemetry-simulator && \
		pytest tests/ -v --cov=. --cov-report=term-missing --cov-fail-under=50
	@echo ""
	@echo "$(GREEN)✅ Simulator tests passed!$(NC)"

test-frontend: ## Run React frontend tests
	@echo ""
	@echo "$(BLUE)═══════════════════════════════════════════════════════$(NC)"
	@echo "$(BLUE)⚛️  Running Frontend Tests (React + TypeScript)$(NC)"
	@echo "$(BLUE)═══════════════════════════════════════════════════════$(NC)"
	@echo ""
	@cd services/telemetry-frontend && \
		npm run test
	@echo ""
	@echo "$(GREEN)✅ Frontend tests passed!$(NC)"

test-e2e: ## Run end-to-end integration tests
	@echo ""
	@echo "$(BLUE)═══════════════════════════════════════════════════════$(NC)"
	@echo "$(BLUE)🔄 Running End-to-End Integration Tests$(NC)"
	@echo "$(BLUE)═══════════════════════════════════════════════════════$(NC)"
	@echo ""
	@echo "Checking if services are running..."
	@if ! docker-compose ps | grep -q "Up"; then \
		echo "⚠️  Services not running. Starting with docker-compose..."; \
		docker-compose up -d; \
		echo "Waiting 10 seconds for services to be ready..."; \
		sleep 10; \
test-coverage: ## Generate coverage reports for all services
	@echo ""
	@echo "$(BLUE)═══════════════════════════════════════════════════════$(NC)"
	@echo "$(BLUE)📊 Generating Coverage Reports$(NC)"
	@echo "$(BLUE)═══════════════════════════════════════════════════════$(NC)"
	@echo ""
	@echo "➜ Python Processor Coverage..."
	@cd services/telemetry-processor && pytest tests/ --cov=. --cov-report=html
	@echo ""
	@echo "➜ Python Simulator Backend Coverage..."
	@cd services/telemetry-simulator-backend && pytest tests/ --cov=. --cov-report=html
	@echo ""
	@echo "➜ Frontend Coverage..."
	@cd services/telemetry-frontend && npm run test:coverage
	@echo ""
	@echo "➜ Simulator Frontend Coverage..."
	@cd services/telemetry-simulator-frontend && npm run test:coverage
	@echo ""
	@echo "$(GREEN)✅ Coverage reports generated!$(NC)"
	@echo ""
	@echo "View reports:"
	@echo "  Processor:          services/telemetry-processor/htmlcov/index.html"
	@echo "  Simulator Backend:  services/telemetry-simulator-backend/htmlcov/index.html"
	@echo "  Frontend:           services/telemetry-frontend/coverage/index.html"
	@echo "  Simulator Frontend: services/telemetry-simulator-frontend/coverage/index.html"
test-clean: ## Clean test artifacts and coverage reports
	@echo "$(BLUE)🧹 Cleaning test artifacts...$(NC)"
	@rm -rf services/telemetry-ingest/build/Testing
	@rm -rf services/telemetry-processor/htmlcov services/telemetry-processor/.coverage services/telemetry-processor/.pytest_cache
	@rm -rf services/telemetry-simulator-backend/htmlcov services/telemetry-simulator-backend/.coverage services/telemetry-simulator-backend/.pytest_cache
	@rm -rf services/telemetry-frontend/coverage
	@rm -rf services/telemetry-simulator-frontend/coverage
	@rm -rf tests/e2e/htmlcov tests/e2e/.coverage tests/e2e/.pytest_cache
	@echo "$(GREEN)✅ Test artifacts cleaned!$(NC)"e reports
	@echo "$(BLUE)🧹 Cleaning test artifacts...$(NC)"
	@rm -rf services/telemetry-ingest/build/Testing
	@rm -rf services/telemetry-processor/htmlcov services/telemetry-processor/.coverage services/telemetry-processor/.pytest_cache
	@rm -rf services/telemetry-simulator/htmlcov services/telemetry-simulator/.coverage services/telemetry-simulator/.pytest_cache
	@rm -rf services/telemetry-frontend/coverage
	@rm -rf tests/e2e/htmlcov tests/e2e/.coverage tests/e2e/.pytest_cache
	@echo "$(GREEN)✅ Test artifacts cleaned!$(NC)"

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
