ci: clean test


.PHONY: clean
clean:
	find smeterd tests -name '__pycache__' -exec rm -rf {} +
	find smeterd tests -name '*.pyc' -exec rm -f {} +
	find smeterd tests -name '*.pyo' -exec rm -f {} +
	find smeterd tests -name '*~' -exec rm -f {} +
	find smeterd tests -name '._*' -exec rm -f {} +
	find smeterd tests -name '.coverage*' -exec rm -f {} +
	rm -rf .tox *.egg dist build .coverage MANIFEST || true


.PHONY: test
test:
	python setup.py test


.PHONY: coverage
coverage:
	coverage run --source smeterd -- setup.py test
	coverage report
	coverage html


# The default make target is ci
.DEFAULT_GOAL := ci
