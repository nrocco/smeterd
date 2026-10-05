ci: clean lint coverage


.PHONY: clean
clean:
	find src tests -name '__pycache__' -exec rm -rf {} +
	find src tests -name '*.pyc' -exec rm -f {} +
	find src tests -name '*.pyo' -exec rm -f {} +
	find src tests -name '*~' -exec rm -f {} +
	find src tests -name '._*' -exec rm -f {} +
	find src tests -name '.coverage*' -exec rm -f {} +
	rm -rf .tox .pytest_cache *.egg *.egg-info dist build htmlcov .coverage MANIFEST


.PHONY: lint
lint:
	uv run ruff check src/ tests/
	uv run ruff format --check src/ tests/


.PHONY: test
test:
	uv run pytest -vv


.PHONY: coverage
coverage:
	uv run pytest -vv --no-cov-on-fail --cov=src --cov-report=term --cov-report=html --cov-report=xml


.PHONY: build
build: clean
	uv build


.DEFAULT_GOAL := ci
