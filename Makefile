#!/usr/bin/make

build: virtualenv lint test

virtualenv: .venv/bin/python
.venv/bin/python:
	sudo apt-get install python-virtualenv
	virtualenv .venv
	.venv/bin/pip install nose flake8 mock pyyaml charmhelpers ansible-lint ansible

lint:.venv/bin/python
	@echo Linting Charm
	@charm proof
	@echo Linting Ansible Routines
	@.venv/bin/ansible-lint playbooks/*
	@.venv/bin/ansible-playbook -i docs/faux-inventory.conf --syntax-check playbooks/site.yaml

clean:
	rm -rf .venv
	find -name *.pyc -delete
