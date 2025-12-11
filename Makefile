.PHONY: help build up down logs clean dev-up dev-down restart ps health

# Colors for output
BLUE := \033[0;34m
GREEN := \033[0;32m
RED := \033[0;31m
NC := \033[0m # No Color

# ============================================================
# Protobuf
# ============================================================

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


proto-simulator-backend: setup-proto ## Generate protobuf files for simulator backend
	@echo "$(BLUE)→ Generating Python protobuf files for simulator backend...$(NC)"
	@mkdir -p $(SIMULATOR_BACKEND_PROTO_DIR)
	@touch $(SIMULATOR_BACKEND_PROTO_DIR)/__init__.py
	protoc -I$(PROTO_SRC_DIR) --python_out=$(SIMULATOR_BACKEND_PROTO_DIR) --pyi_out=$(SIMULATOR_BACKEND_PROTO_DIR) $(PROTO_SRC_DIR)/enums.proto
	protoc -I$(PROTO_SRC_DIR) --python_out=$(SIMULATOR_BACKEND_PROTO_DIR) --pyi_out=$(SIMULATOR_BACKEND_PROTO_DIR) $(PROTO_SRC_DIR)/packet_definitions.proto
	@echo "$(GREEN)  ✓ Backend protobuf files generated in $(SIMULATOR_BACKEND_PROTO_DIR)$(NC)"
		

proto-simulator-frontend: setup-proto ## Generate protobuf files for simulator frontend (using ts-proto)
	@echo "$(BLUE)→ Generating TypeScript protobuf files for simulator frontend...$(NC)"
	@mkdir -p $(SIMULATOR_FRONTEND_PROTO_DIR)
	@cd services/telemetry-simulator-frontend && \
		if [ ! -d "node_modules" ]; then \
			echo "$(BLUE)  → Installing npm dependencies...$(NC)"; \
			npm install; \
		fi && \
		if [ ! -f "node_modules/.bin/protoc-gen-ts_proto" ]; then \
			echo "$(BLUE)  → Installing ts-proto...$(NC)"; \
			npm install --save-dev ts-proto; \
		fi && \
		protoc --plugin=./node_modules/.bin/protoc-gen-ts_proto --ts_proto_out=./src/proto \
			--ts_proto_opt=esModuleInterop=true \
			--ts_proto_opt=outputClientImpl=false \
			-I../../$(PROTO_SRC_DIR) \
			../../$(PROTO_SRC_DIR)/enums.proto \
			../../$(PROTO_SRC_DIR)/packet_definitions.proto
	@echo "$(GREEN)  ✓ Frontend protobuf files generated in $(SIMULATOR_FRONTEND_PROTO_DIR)$(NC)"

proto: proto-simulator-backend proto-simulator-frontend ## Generate all protobuf files
	@echo "$(BLUE)Generating protobuf files for F1 $(F1_GAME_VERSION)...$(NC)"
	@echo ""
	@$(MAKE) proto-simulator-backend
	@echo ""
	@$(MAKE) proto-simulator-frontend
	@echo ""
	@echo "$(GREEN)✅ All protobuf files generated!$(NC)"
