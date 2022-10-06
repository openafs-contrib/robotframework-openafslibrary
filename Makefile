# Copyright (c) 2018 Sine Nomine Associates

help:
	@echo "usage: make <target> [<target> ...]"
	@echo ""
	@echo "Packaging targets:"
	@echo "  sdist          create source distribution"
	@echo "  wheel          create wheel distribution"
	@echo "  rpm            create rpm package"
	@echo "  deb            create deb package"
	@echo "  upload         upload packages to pypi.org"
	@echo ""
	@echo "Installation targets:"
	@echo "  install        install package"
	@echo "  uninstall      uninstall package"
	@echo "  install-user   user mode install"
	@echo "  uninstall-user user mode uninstall"
	@echo "  install-dev    developer mode install"
	@echo "  uninstall-dev  developer mode uninstall"
	@echo ""
	@echo "Development targets:"
	@echo "  init           initialize development environment"
	@echo "  lint           run python linter"
	@echo "  checkdocs      validate documents"
	@echo "  docs           generate documents"
	@echo "  test           run unit tests"
	@echo "  clean          delete generated files"
	@echo "  distclean      delete generated and config files"

include Makefile.config

VIRTUAL_ENV ?= .venv

.venv:
	$(PYTHON) -m venv .venv
	.venv/bin/pip install -U pip wheel
	.venv/bin/pip install -r requirements.txt

OpenAFSLibrary/__version__.py:
	echo "VERSION = '$(VERSION)'" >$@

init: .venv OpenAFSLibrary/__version__.py

source = \
  OpenAFSLibrary/command.py  \
  OpenAFSLibrary/__init__.py \
  OpenAFSLibrary/variable.py \
  OpenAFSLibrary/keywords/acl.py \
  OpenAFSLibrary/keywords/cache.py \
  OpenAFSLibrary/keywords/command.py \
  OpenAFSLibrary/keywords/dump.py \
  OpenAFSLibrary/keywords/__init__.py \
  OpenAFSLibrary/keywords/login.py \
  OpenAFSLibrary/keywords/pag.py \
  OpenAFSLibrary/keywords/path.py \
  OpenAFSLibrary/keywords/rx.py \
  OpenAFSLibrary/keywords/volume.py

lint: init
	$(VIRTUAL_ENV)/bin/pyflakes $(source)

checkdocs: init # requires collective.checkdocs
	$(VIRTUAL_ENV)/bin/python setup.py checkdocs

.PHONY: doc docs
doc docs: init
	$(MAKE) -C docs librst html

test: init
	$(VIRTUAL_ENV)/bin/python -m unittest -v test

sdist: init
	$(VIRTUAL_ENV)/bin/python setup.py sdist

wheel: init
	$(VIRTUAL_ENV)/bin/python setup.py bdist_wheel

rpm: init
	$(VIRTUAL_ENV)/bin/python setup.py bdist_rpm

deb: init
	$(VIRTUAL_ENV)/bin/python setup.py --command-packages=stdeb.command bdist_deb

upload: sdist wheel
	.venv/bin/twine upload dist/*

install: init
	$(MAKE) -f Makefile.$(INSTALL) $@

install-user: init
	$(MAKE) -f Makefile.$(INSTALL) $@

install-dev: init
	$(MAKE) -f Makefile.$(INSTALL) $@

uninstall:
	$(MAKE) -f Makefile.$(INSTALL) $@

uninstall-user:
	$(MAKE) -f Makefile.$(INSTALL) $@

uninstall-dev:
	$(MAKE) -f Makefile.$(INSTALL) $@

clean:
	rm -f *.pyc test/*.pyc OpenAFSLibrary/*.pyc OpenAFSLibrary/keywords/*.pyc
	rm -fr $(NAME).egg-info/ build/ dist/
	rm -fr $(NAME)*.tar.gz deb_dist/
	rm -f MANIFEST

distclean: clean
	rm -f OpenAFSLibrary/__version__.py
	rm -f Makefile.config
	rm -f files.txt
