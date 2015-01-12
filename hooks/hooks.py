#!/usr/bin/env python

import sys
import setup

setup.pre_install()

import charmhelpers.contrib.ansible

# Create the hooks helper, passing a list of hooks which will be
# handled by default by running all sections of the playbook
# tagged with the hook name.
hooks = charmhelpers.contrib.ansible.AnsibleHooks(
    playbook_path='playbooks/site.yaml',
    default_hooks=[
        'start',
        'stop',
        'config-changed',
        'upgrade-charm',
        'db-relation-changed',
        'network-relation-changed'
    ])


@hooks.hook('install', 'upgrade-charm')
def install():
    """Install ansible.

    The hook() helper decorating this install function ensures that after this
    function finishes, any tasks in the playbook tagged with install or
    upgrade-charm are executed.
    """
    charmhelpers.contrib.ansible.install_ansible_support(from_ppa=True)


if __name__ == "__main__":
    hooks.execute(sys.argv)
