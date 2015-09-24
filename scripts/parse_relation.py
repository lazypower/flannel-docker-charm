#!/usr/bin/python

import yaml

path='/etc/ansible/host_vars/localhost'

with open(path, 'r') as f:
    data = yaml.safe_load(f)

try:
  print data['relations']['network'][0]['__relid__']
except:
  pass
