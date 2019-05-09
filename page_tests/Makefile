PYTHON_INTERPRETER=python3
VENV_PATH=.venv
PIP=$(VENV_PATH)/bin/pip
BOUSSOLE=$(VENV_PATH)/bin/boussole
OPTIMUS=$(VENV_PATH)/bin/optimus-cli
FLAKE=$(VENV_PATH)/bin/flake8
PYTEST=$(VENV_PATH)/bin/pytest
PACKAGE_NAME=django_palette

help:
	@echo "Please use \`make <target>' where <target> is one of"
	@echo
	@echo "  install             -- to install this project with virtualenv and Pip"
	@echo ""
	@echo "  clean               -- to clean EVERYTHING (Warning)"
	@echo "  clean-pycache       -- to remove all __pycache__, this is recursive from current directory"
	@echo "  clean-install       -- to clean Python side installation"
	@echo "  clean-build         -- to clean project builds for every environnement"
	@echo ""
	@echo "  html                -- to build project from template sources with default environnement"
	@echo "  html-prod           -- to build project from template sources with production environnement"
	@echo "  watch-html          -- to launch project watcher with default environnement"
	@echo ""
	@echo "  build                -- to build everything (HTML, CSS, PO) with default environnement"
	@echo "  build-prod           -- to build everything (HTML, CSS, PO) with production environnement"
	@echo ""
	@echo "  css                 -- to build CSS with default environnement"
	@echo "  watch-css           -- to launch watcher CSS with default environnement"
	@echo ""
	@echo "  po                  -- to update PO files (translations catalogs) from template sources"
	@echo "  mo                  -- to build MO files (compiled translations catalogs) from PO files"
	@echo ""
	@echo "  run                 -- to launch local server on 0.0.0.0:8001 with default environnement (using CherryPy)"
	@echo "  run-prod            -- to launch local server on 0.0.0.0:8001 with production environnement"
	@echo

clean-pycache:
	rm -Rf .pytest_cache
	find . -type d -name "__pycache__"|xargs rm -Rf
	find . -name "*\.pyc"|xargs rm -f
.PHONY: clean-pycache

clean-install:
	rm -Rf $(VENV_PATH)
.PHONY: clean-install

clean-build:
	rm -Rf _build
.PHONY: clean-build

clean: clean-install clean-build clean-pycache
.PHONY: clean

venv:
	virtualenv -p $(PYTHON_INTERPRETER) $(VENV_PATH)
	# This is required for those ones using ubuntu<16.04
	$(PIP) install --upgrade pip
	$(PIP) install --upgrade setuptools
.PHONY: venv

install: venv
	$(PIP) install -r requirements.txt
.PHONY: install

po:
	$(OPTIMUS) po --update
.PHONY: po

mo:
	$(OPTIMUS) po --compile
.PHONY: mo

css:
	$(BOUSSOLE) compile --config boussole.json
.PHONY: css

watch-sass:
	$(BOUSSOLE) watch --config boussole.json
.PHONY: watch-sass

html:
	$(OPTIMUS) build
.PHONY: html

watch-html:
	$(OPTIMUS) watch
.PHONY: watch-html

html-prod:
	$(OPTIMUS) build --settings-name settings/production
.PHONY: html-prod

build: mo css html
.PHONY: build

build-prod: mo css html-prod
.PHONY: build-prod

run:
	$(OPTIMUS) runserver 0.0.0.0:8001
.PHONY: run

run-prod:
	$(OPTIMUS) runserver 0.0.0.0:8001 --settings-name settings/production
.PHONY: run-prod

flake:
	$(FLAKE) --show-source .
.PHONY: flake

tests:
	$(PYTEST) -vv --exitfirst tests/
.PHONY: tests

quality: tests flake
.PHONY: quality
