PYTHON_INTERPRETER=python3
VENV_PATH=.venv
PIP=$(VENV_PATH)/bin/pip
FLAKE=$(VENV_PATH)/bin/flake8
PYTEST=$(VENV_PATH)/bin/pytest
PACKAGE_NAME=py_website_capture

help:
	@echo "Please use \`make <target>' where <target> is one of"
	@echo
	@echo "  install             -- to install this project with virtualenv and Pip"
	@echo ""
	@echo "  clean               -- to clean EVERYTHING (Warning)"
	@echo "  clean-pycache       -- to remove all __pycache__, this is recursive from current directory"
	@echo "  clean-install       -- to clean Python side installation"
	@echo "  clean-build         -- to clean screenshot outputs"
	@echo ""
	@echo "  flake               -- to launch Flake8 checking"
	@echo "  tests               -- to launch base test suite using Pytest"
	@echo "  tests-drivers       -- to launch drivers test suite using Pytest"
	@echo "  tests-all       -- to launch every tests suites using Pytest"
	@echo "  quality             -- to launch Flake8 checking and every tests suites"
	@echo

clean-pycache:
	rm -Rf .pytest_cache
	find . -type d -name "__pycache__"|xargs rm -Rf
	find . -name "*\.pyc"|xargs rm -f
.PHONY: clean-pycache

clean-install:
	rm -Rf $(VENV_PATH)
	rm -Rf $(PACKAGE_NAME).egg-info
.PHONY: clean-install

clean-build:
	rm -Rf outputs
	rm -Rf *.log
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
	$(PIP) install -e .[cli,dev]
	mkdir -p outputs
	@echo "You will need a WebDriver like 'geckodriver' or 'chromedriver'"
.PHONY: install

flake:
	$(FLAKE) --show-source $(PACKAGE_NAME)
.PHONY: flake

tests:
	$(PYTEST) -vv --exitfirst tests/
.PHONY: tests

tests-drivers:
	$(PYTEST) -vv --exitfirst drivers_tests/
.PHONY: tests-drivers

tests-all: tests tests-drivers
.PHONY: tests-all

quality: tests-all flake
.PHONY: quality
