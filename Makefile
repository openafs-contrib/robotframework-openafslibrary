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
	@echo "  lint           run python linter"
	@echo "  checkdocs      validate documents"
	@echo "  docs           generate documents"
	@echo "  test           run unit tests"
	@echo "  clean          delete generated files"
	@echo "  distclean      delete generated and config files"

include Makefile.config

generated: OpenAFSLibrary/__version__.py

OpenAFSLibrary/__version__.py:
	echo "VERSION = '$(VERSION)'" >$@

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

lint: generated
	$(PYFLAKES) $(source)

checkdocs: generated # requires collective.checkdocs
	$(PYTHON) setup.py checkdocs

.PHONY: doc docs
doc docs: generated
	$(MAKE) -C docs librst html

test: generated
	$(PYTHON) -m unittest -v test

sdist: generated
	$(PYTHON) setup.py sdist

wheel: generated
	$(PYTHON) setup.py bdist_wheel

rpm: generated
	$(PYTHON) setup.py bdist_rpm

deb: generated
	$(PYTHON) setup.py --command-packages=stdeb.command bdist_deb

upload: sdist wheel
	twine upload dist/*

install: generated
	$(MAKE) -f Makefile.$(INSTALL) $@

install-user: generated
	$(MAKE) -f Makefile.$(INSTALL) $@

install-dev: generated
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
