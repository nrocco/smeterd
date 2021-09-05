ci: clean lint test


.PHONY: clean
clean:
	find smeterd tests -name '__pycache__' -exec rm -rf {} +
	find smeterd tests -name '*.pyc' -exec rm -f {} +
	find smeterd tests -name '*.pyo' -exec rm -f {} +
	find smeterd tests -name '*~' -exec rm -f {} +
	find smeterd tests -name '._*' -exec rm -f {} +
	find smeterd tests -name '.coverage*' -exec rm -f {} +
	rm -rf .tox *.egg dist build .coverage MANIFEST || true


.PHONY: lint
lint:
	flake8

.PHONY: test
test:
	pytest


.PHONY: coverage
coverage:
	pytest --no-cov-on-fail --cov=smeterd --cov-report=term --cov-report=html tests/


# The default make target is ci
.DEFAULT_GOAL := ci
