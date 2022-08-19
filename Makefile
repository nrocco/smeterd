MODULE = smeterd


ci: clean lint coverage


.PHONY: clean
clean:
	find $(MODULE) tests -name '__pycache__' -exec rm -rf {} +
	find $(MODULE) tests -name '*.pyc' -exec rm -f {} +
	find $(MODULE) tests -name '*.pyo' -exec rm -f {} +
	find $(MODULE) tests -name '*~' -exec rm -f {} +
	find $(MODULE) tests -name '._*' -exec rm -f {} +
	find $(MODULE) tests -name '.coverage*' -exec rm -f {} +
	rm -rf .tox *.egg dist build .coverage MANIFEST || true


.PHONY: lint
lint:
	flake8


.PHONY: test
test:
	python -m pytest -vv


.PHONY: coverage
coverage:
	python -m pytest -vv --no-cov-on-fail --cov=$(MODULE) --cov-report=html --cov-report=term tests/


.PHONY: build
build: clean
	python -m build --no-isolation


.DEFAULT_GOAL := ci
