#!/usr/bin/make


build: tox lint test

virtualenv:
	virtualenv .venv

tox:
/usr/bin/tox:
	sudo apt-get install -y  python-tox python-dev python-virtualenv

lint: /usr/bin/tox
	tox -e lint


unit_test: /usr/bin/tox
	@# tox
	@echo "Unit tests pending"

clean:
	rm -rf .venv .tox
	find -name *.pyc -delete
