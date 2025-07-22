.PHONY: help build install uninstall test clean dev-install dist release-build all dev

help:  ## Show this help message
	@echo "Tarot CLI Development Commands"
	@echo "=============================="
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-15s %s\n", $$1, $$2}'

build:  ## Build the tarot executable
	uv run python build.py

install: build  ## Build and install tarot CLI locally
	./install.sh

uninstall:  ## Uninstall tarot CLI
	./uninstall.sh

test:  ## Run tests
	uv run pytest -v

typecheck:  ## Run type checking
	uv run mypy -m src.models -m src.draws -m src.main -m src.intent -m src.builders

clean:  ## Clean build artifacts
	rm -rf dist/ build/ *.spec

dev-install:  ## Install development dependencies
	uv sync

dev: dev-install  ## Set up development environment
	@echo "Development environment ready!"
	@echo "Run 'make build' to create executable"
	@echo "Run 'make install' to build and install"

dist: clean build  ## Build distribution executable

release-build: clean dev-install typecheck test build  ## Full release build with all checks

all: dev-install typecheck test build  ## Run full development workflow
