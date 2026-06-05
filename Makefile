# ClipMind Makefile

.PHONY: help install dev test clean build lint format

help:
	@echo "🧠 ClipMind - Available commands:"
	@echo ""
	@echo "  make install    Install ClipMind"
	@echo "  make dev        Install in development mode"
	@echo "  make test       Run unit tests"
	@echo "  make clean      Clean build artifacts"
	@echo "  make build      Build distribution packages"
	@echo "  make run        Run ClipMind TUI"
	@echo "  make monitor    Start clipboard monitor"
	@echo ""

install:
	pip install .

dev:
	pip install -e .

test:
	python -m unittest discover -s tests -v

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf __pycache__/
	rm -rf .pytest_cache/
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -type d -delete

build: clean
	python -m build

run:
	python -m clipmind

monitor:
	python -m clipmind --monitor
