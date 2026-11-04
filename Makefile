.DEFAULT_GOAL := help

# The API runs in a virtualenv at api/.venv (created by `make install`).
VENV := api/.venv
PY   := $(VENV)/bin/python

.PHONY: help install install-api install-ui dev dev-api dev-ui build build-ui build-lambda test test-api test-ui clean

help: ## Show available commands
	@grep -E '^[a-zA-Z_-]+:.*## ' $(MAKEFILE_LIST) | awk -F':.*## ' '{printf "  \033[36m%-14s\033[0m %s\n", $$1, $$2}'

install: install-api install-ui ## Install all dependencies (api venv + ui workspace)

install-api: ## Create api/.venv and install the API's Python dependencies
	python3 -m venv $(VENV)
	$(PY) -m pip install -r api/requirements-dev.txt

install-ui: ## Install the UI's npm dependencies
	npm install

# --- Dev -------------------------------------------------------------------

dev: ## Run API (:3000) and UI (:5173) together
	npm run dev

dev-api: ## Run only the API
	npm run dev:api

dev-ui: ## Run only the UI
	npm run dev:ui

# --- Build (for hosting) ---------------------------------------------------

build: build-ui build-lambda ## Build everything for hosting

build-ui: ## Build the static UI to ui/dist
	npm run build -w ui

build-lambda: ## Bundle the API for AWS Lambda to api/dist-lambda
	./scripts/build-lambda.sh

# --- Test ------------------------------------------------------------------

test: test-api test-ui ## Run all tests

test-api: ## Run API tests (pytest)
	cd api && .venv/bin/python -m pytest

test-ui: ## Run UI tests (Vitest)
	npm test -w ui

# --- Housekeeping ----------------------------------------------------------

clean: ## Remove build output
	rm -rf api/dist-lambda ui/dist terraform/.build
