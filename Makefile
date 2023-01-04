.PHONY: clean
clean:
	rm -rf dist/ var/
	find src/ tests/ -name __pycache__ -exec rm -rf {} \; 

.PHONY: install
install: requirements.txt
	python3 -m pip install -U pip wheel build twine
	python3 -m pip install -r requirements.txt

.PHONY: test
test:
	python3 -m pytest

.PHONY: lint
lint:
	pylint -E src/

.PHONY: format
format:
	black src/ tests/

.PHONY: build
build:
	python3 -m build

.PHONY: upload
upload:
	python3 -m twine upload dist/*
