#!/usr/bin/make

build: virtualenv lint test

virtualenv: .venv/bin/python
.venv/bin/python:
	sudo apt-get install python-virtualenv
	virtualenv .venv
	.venv/bin/pip install nose flake8 mock pyyaml charmhelpers

lint:
	@.venv/bin/flake8 hooks unit_tests
	@charm proof

test: virtualenv
	@echo Starting tests...
	@CHARM_DIR=. PYTHONPATH=./hooks .venv/bin/nosetests --nologcapture unit_tests

clean:
	rm -rf .venv
	find -name *.pyc -delete
