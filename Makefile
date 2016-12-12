prefix ?= /usr

VIRTUAL_ENV ?= $(PWD)/env

PY = $(VIRTUAL_ENV)/bin/python
PIP = $(VIRTUAL_ENV)/bin/pip

PACKAGE = smeterd


$(PY):
	pyvenv env
	$(eval VIRTUAL_ENV = $(PWD)/env)


.PHONY: dist
dist: $(PY) test
	$(PY) setup.py sdist


.PHONY: develop
develop: $(PY)
	$(PY) setup.py develop


.PHONY: install
install:
	$(PY) setup.py install --prefix="$(prefix)" --root="$(DESTDIR)" --optimize=1


.PHONY: deps
deps: $(PY)
	if [ -f requirements.txt ]; then $(PIP) install -r requirements.txt; fi


.PHONY: test
test: $(PY)
	$(PY) setup.py test


.PHONY: bump
bump: $(PY)
	@echo "Current $(PACKAGE) version is: $(shell $(PY) setup.py --version)"
	@test ! -z "$(version)" || ( echo "specify a version number: make bump version=X.X.X" && exit 1 )
	@! git status --porcelain 2> /dev/null | grep -v "^??" || ( echo 'uncommited changes. commit them first' && exit 1 )
	@echo "Bumping to $(version)"
	sed -i'.bak' -e "/^__version__ = .*$$/s/'[^']*'/'$(version)'/" $(PACKAGE)/__init__.py
	rm -f $(PACKAGE)/__init__.py.bak
	git add $(PACKAGE)/__init__.py
	git commit -m 'Bumped version number to $(version)'
	git tag $(version)
	@echo "Version $(version) commited and tagged. Don't forget to push to github."


.PHONY: clean
clean:
	find $(PACKAGE) -name '*.pyc' -exec rm -f {} +
	find $(PACKAGE) -name '*.pyo' -exec rm -f {} +
	find $(PACKAGE) -name '*~' -exec rm -f {} +
	find $(PACKAGE) -name '._*' -exec rm -f {} +
	find $(PACKAGE) -name '.coverage*' -exec rm -f {} +
	rm -rf .tox *.egg dist build .coverage MANIFEST || true


.PHONY: upload
upload: $(PY) clean test
	$(PY) setup.py sdist register upload
