VENV := .venv
PYTHON := $(VENV)/bin/python

.PHONY: install lint typecheck test check run run-mock clean

install:
	python3 -m venv $(VENV)
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install -e ".[dev]"

lint:
	$(PYTHON) -m ruff check .

typecheck:
	$(PYTHON) -m mypy src

test:
	$(PYTHON) -m pytest

check: lint typecheck test

run:
	$(PYTHON) -m uvicorn vinyl_set_builder.main:app --reload

run-mock:
	VINYL_SEED_MOCKS=1 $(PYTHON) -m uvicorn vinyl_set_builder.main:app --reload

clean:
	rm -rf .pytest_cache .mypy_cache .ruff_cache
	find . -type d -name "__pycache__" -exec rm -rf {} +
