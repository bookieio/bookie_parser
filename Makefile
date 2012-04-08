# Makefile to help automate tasks
WD := $(shell pwd)
PY := bin/python
PEP8 := bin/pep8
PIP := bin/pip
PIP_MIR = PIP_FIND_LINKS='http://mypi http://simple.crate.io/'
NOSE := bin/nosetests
GUNICORN := bin/gunicorn

.PHONY: all
all: deps

.PHONY: deps
deps: venv
	@echo "\n\nSilently installing packages (this will take a while)..."
	$(PIP_MIR) $(PIP) install -q -r requirements.txt

venv: bin/python
bin/python:
	virtualenv .

.PHONY: clean_venv
clean_venv:
	rm -rf lib include local bin

develop: lib/python*/site-packages/bookie_parser.egg-link
lib/python*/site-packages/bookie_parser.egg-link:
	$(PY) setup.py develop
