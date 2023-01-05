.PHONY: clean
clean:
	@echo === Clean ===
	rm -rf dist/ var/ .coverage/ .pytest_cache
	find src/ tests/ -name __pycache__ -exec rm -rf {} \; 


.PHONY: pre-install
pre-install:
	@echo === Pre-install ===
	python3 -m pip install -U pip wheel pip-tools


requirements.txt: pyproject.toml
	@echo === requirements.txt ===
	python3 -m piptools compile --resolver=backtracking --output-file requirements.txt pyproject.toml


requirements-dev.txt: pyproject.toml
	@echo === requirements-dev.txt ===
	python3 -m piptools compile --resolver=backtracking --extra dev --output-file requirements-dev.txt pyproject.toml


.PHONY: install
install: pre-install requirements.txt
	@echo === Install ===
	python3 -m pip install -r requirements.txt


.PHONY: install-dev
install-dev: pre-install requirements-dev.txt
	@echo === Install Dev ===
	python3 -m pip install -r requirements-dev.txt


.PHONY: test
test:
	@echo === Test ===
	python3 -m pytest


.PHONY: lint
lint:
	@echo === Lint ===
	python3 -m pylint --disable=R,C src/


.PHONY: format
format:
	@echo === Format ===
	python3 -m black src/ tests/


.PHONY: build
build:
	@echo === Build ===
	python3 -m build


.PHONY: upload
upload:
	@echo === Upload ===
	python3 -m twine upload dist/*
