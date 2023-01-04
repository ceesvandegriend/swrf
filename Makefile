.PHONY: clean
clean:
	rm -rf dist/ var/
	find src/ tests/ -name __pycache__ -exec rm -rf {} \; 

.PHONY: format
format:
	black src/ tests/

.PHONY: lint
lint:
	pylint -E src/

.PHONY: install
install: requirements.txt
	python3 -m pip install -U pip wheel
	python3 -m pip install -r requirements.txt

.PHONY: test
test:
	pytest --cov
