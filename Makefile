VIRTUAL_ENV ?= $(PWD)/env

PY = $(VIRTUAL_ENV)/bin/python
PIP = $(VIRTUAL_ENV)/bin/pip

PACKAGE = smeterd


$(PY):
	virtualenv env
	$(eval VIRTUAL_ENV = $(PWD)/env)


build: $(PY)
	$(PY) setup.py test sdist


develop: $(PY)
	$(PY) setup.py develop


deps: $(PY)
	if [ -f requirements.txt ]; then $(PIP) install -r requirements.txt; fi


test: $(PY)
	$(PY) setup.py test


bump:
	@echo "Current $(PACKAGE) version is: $(shell sed -E "s/__version__ = .([^']+)./\\1/" $(PACKAGE)/__init__.py)"
	@test ! -z "$(version)" || ( echo "specify a version number: make bump version=X.X.X" && exit 1 )
	@! git status --porcelain 2> /dev/null | grep -v "^??" || ( echo 'uncommited changes. commit them first' && exit 1 )
	@echo "Bumping to $(version)"
	sed -i'.bak' -e "/^__version__ = .*$$/s/'[^']*'/'$(version)'/" $(PACKAGE)/__init__.py
	rm -f $(PACKAGE)/__init__.py.bak
	git add $(PACKAGE)/__init__.py
	git commit -m 'Bumped version number to $(version)'
	git tag $(version)
	@echo "Version $(version) commited and tagged. Don't forget to push to github."


clean:
	find $(PACKAGE) -name '*.pyc' -exec rm -f {} +
	find $(PACKAGE) -name '*.pyo' -exec rm -f {} +
	find $(PACKAGE) -name '*~' -exec rm -f {} +
	find $(PACKAGE) -name '._*' -exec rm -f {} +
	find $(PACKAGE) -name '.coverage*' -exec rm -f {} +
	rm -rf build/ dist/ MANIFEST 2>/dev/null || true


upload: $(PY)
	$(PY) setup.py test sdist register upload


.PHONY: build develop deps test bump clean upload
