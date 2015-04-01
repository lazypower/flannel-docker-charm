#!/usr/bin/make

build: virtualenv lint

virtualenv: .venv/bin/python
.venv/bin/python:
	virtualenv .venv
	.venv/bin/pip install nose flake8 mock pyyaml charmhelpers ansible-lint ansible

lint:.venv/bin/python
	@echo Linting Charm
	@charm proof
	@echo Linting Ansible Routines
	@.venv/bin/ansible-lint playbooks/*

clean:
	rm -rf .venv
	find -name *.pyc -delete
