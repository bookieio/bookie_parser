# Makefile to help automate tasks
WD := $(shell pwd)
PY := bin/python
PEP8 := bin/pep8
PIP := bin/pip
PIP_MIR = PIP_FIND_LINKS='http://mypi http://simple.crate.io/'
NOSE := bin/nosetests
PYSCSS := bin/pyscss
GUNICORN := bin/gunicorn
CSS := bin/pyscss


# #######
# INSTALL
# #######
.PHONY: all
all: venv deps css

.PHONY: clean_all
clean_all: clean_venv

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


# ###########
# Tests rule!
# ###########
.PHONY: test
test: $(NOSE)
	$(NOSE) --with-id -s -x bookie_parser/tests

$(NOSE):
	$(PIP) install nose pep8 coverage WebTest


# ###########
# Development
# ###########
.PHONY: css
css: bookie_parser/static/styles.css

bookie_parser/static/styles.css:
	$(PYSCSS) -I bookie_parser/static/ -o bookie_parser/static/styles.css bookie_parser/static/styles.scss

.PHONY: clean_css
clean_css:
	- rm bookie_parser/static/styles.css

.PHONY: run
run: run_css run_app

.PHONY: run_css
run_css:
	$(PYSCSS) --watch bookie_parser/static &

.PHONY: run_app
run_app:
	pserve --reload --monitor-restart development.ini

.PHONY: stop
stop:
	kill -9 `cat app.pid` || true
	rm app.pid || true


.PHONY: lint
lint: bin/flake8
	flake8 bookie_parser

bin/flake8:
	$(PIP) install flake8


# ###############
# Heroku controls
# ###############

.PHONY: heroku
heroku:
	git push heroku master

.PHONY: foreman
foreman:
	foreman start
