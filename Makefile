# Makefile to help automate tasks
WD := $(shell pwd)
PY := bin/python
PEP8 := bin/pep8
PIP := bin/pip
PIP_MIR = PIP_FIND_LINKS='http://mypi http://simple.crate.io/'
NOSE := bin/nosetests
GUNICORN := bin/gunicorn
CSS := bin/pyscss

.PHONY: clean_all
clean_all: clean_venv


# ###########
# Tests rule!
# ###########
.PHONY: test
test:
	$(NOSE) --with-id -s -x bookie_parser/tests

# #######
# INSTALL
# #######
.PHONY: all
all: venv deps css

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
# Development
# ###########
.PHONY: css
css: base.css

base.css:
	wget "https://bmark.us/static/css/readable.scss" -O bookie_parser/static/readable.scss
	$(CSS) -I bookie_parser/static/ -o bookie_parser/static/base.css bookie_parser/static/base.scss

.PHONY: run
run:
	gunicorn -k tornado -p app.pid bookie_parser &

.PHONY: stop
stop:
	kill -9 `cat app.pid` || true
	rm app.pid || true


# ###############
# Heroku controls
# ###############

.PHONY: heroku
heroku:
	git push heroku master

.PHONY: foreman
foreman:
	foreman start
