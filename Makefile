VIRTUAL_ENV ?= $(PWD)/env

PY = $(VIRTUAL_ENV)/bin/python
PIP = $(VIRTUAL_ENV)/bin/pip
NOSE = $(VIRTUAL_ENV)/bin/nosetests
COVERAGE = $(VIRTUAL_ENV)/bin/coverage
SPHINXBUILD = $(VIRTUAL_ENV)/bin/sphinx-build

current_version = $(shell $(PY) setup.py --version)
package_name = $(shell $(PY) setup.py --name)
init_py_file = $(package_name)/__init__.py


# Create a virtualenv if not in one already
$(PY):
	virtualenv env
	$(eval VIRTUAL_ENV = $(PWD)/env)

# Install sphinx to generate documentation
$(SPHINXBUILD): $(PY)
	$(PIP) install sphinx

# Install dependencies need for testing
$(NOSE): $(PY)
	$(PIP) install nose

# Install the coverage module
$(COVERAGE): $(PY)
	$(PIP) install coverage


# Build the source tarball
.PHONY: build
build: $(PY) test clean
	$(PY) setup.py sdist


# Prepare the environment for development
.PHONY: develop
develop: $(PY) deps
	$(PY) setup.py develop


# Generate documentation
.PHONY: docs
docs: $(PY) $(SPHINXBUILD)
	cd docs/; $(MAKE) html SPHINXBUILD=$(SPHINXBUILD)


# Upload package to PyPi
.PHONY: upload
upload: $(PY) test clean
	$(PY) setup.py sdist register upload


# Upload Sphinx documentation to http://pythonhosted.org
.PHONY: upload_docs
upload_docs: $(PY) test clean docs
	$(PY) setup.py upload_docs --upload-dir docs/_build/html/


# install development dependencies
.PHONY: deps
deps: $(PY)
	if [ -f requirements.txt ]; then $(PIP) install -r requirements.txt; fi


# run all tests with nosetests
.PHONY: test
test: $(PY) deps $(NOSE)
	$(NOSE)


.PHONY: coverage
coverage: $(PY) deps $(NOSE) $(COVERAGE)
	$(NOSE) --with-coverage --cover-package=$(package_name)


# bump the version number
.PHONY: bump
bump: $(PY)
	@test ! -z "$(version)" || ( echo "specify a version number: make bump version=$(current_version)" && exit 1 )
	@! git status --porcelain 2> /dev/null | grep -v "^??" || ( echo 'uncommited changes. commit them first' && exit 1 )
	@echo "Bumping current version $(current_version) to $(version)"
	sed -i'.bak' -e "/^__version__ = .*$$/s/'[^']*'/'$(version)'/" $(init_py_file)
	rm -f $(init_py_file).bak
	git add $(init_py_file)
	git commit -m 'Bumped version number to $(version)'
	git tag -m 'Mark stable release version $(version)' -a $(version)
	@echo "Version $(version) commited and tagged. You can 'make push' or 'make upload' now :)"


# Fetch everything from github
.PHONY: fetch
fetch:
	git fetch --all
	git fetch --tags


# Push to github but run tests first
.PHONY: push
push: test
	git push origin HEAD
	git push origin --tags


# Clean all build artifacts
.PHONY: clean
clean:
	find $(package_name) -name '*.pyc' -exec rm -f {} +
	find $(package_name) -name '*.pyo' -exec rm -f {} +
	find $(package_name) -name '*~' -exec rm -f {} +
	find $(package_name) -name '._*' -exec rm -f {} +
	find $(package_name) -name '.coverage*' -exec rm -f {} +
	rm -rf build/ dist/ MANIFEST docs/_build/* 2>/dev/null || true


.PHONY: tags
tags:
	ctags --languages=python --recurse --python-kinds=-i --exclude=.git --totals=yes $(package_name)/
