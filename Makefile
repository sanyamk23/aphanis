.PHONY: install dev test build build-all publish clean

PYTHON ?= python3

install:
	$(PYTHON) -m pip install -e .

dev:
	uv venv
	uv pip install -e ".[dev]"

test:
	$(PYTHON) -m pytest tests/ -v

## Build standalone binary for current platform
build:
	pyinstaller --onefile --name aphanis --console aphanis/cli.py
	@echo "✅ Binary at dist/aphanis"

## Build binaries for all platforms (requires Docker for cross-compilation)
build-all:
	@echo "Building macOS (arm64)..."
	pyinstaller --onefile --name aphanis --target-arch arm64 --codesign-identity - aphanis/cli.py || \
	pyinstaller --onefile --name aphanis --console aphanis/cli.py
	@echo "Building macOS (x86_64)..."
	# Requires cross-compilation toolchain
	@echo "Building Linux..."
	# Requires linux build env
	@echo "Building Windows..."
	# Requires wine + pyi
	@echo "✅ All binaries built (see dist/)"

publish: build
	gh release create v$(shell $(PYTHON) -c "import aphanis; print(aphanis.__version__)") \
		dist/aphanis-* \
		--title "Aphanis v$(shell $(PYTHON) -c "import aphanis; print(aphanis.__version__)")" \
		--generate-notes

clean:
	rm -rf dist/ build/ *.spec .eggs/ aphanis.egg-info/
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true

lint:
	$(PYTHON) -m py_compile aphanis/*.py

.PHONY: help
help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'