#!/usr/bin/env python3

# This is an integration test for the flannel-docker charm.

import amulet
import unittest

seconds = 900


class TestDeployment(unittest.TestCase):
    """
    Create a unit test style class for this amulet test.
    """
    @classmethod
    def setUpClass(cls):
        """
        The setup method runs once after the class is created.
        """
        cls.deployment = amulet.Deployment(series='trusty')

        cls.deployment.add('docker', 'cs:trusty/docker')
        cls.deployment.add('flannel-docker')
        cls.deployment.add('etcd', 'cs:~hazmat/trusty/etcd')

        cls.deployment.configure('docker', {})
        cls.deployment.configure('etcd', {})
        cls.deployment.configure('flannel-docker', {})

        cls.deployment.relate('flannel-docker:docker-host', 'docker:juju-info')
        cls.deployment.relate('flannel-docker:db', 'etcd:client')
        cls.deployment.relate('flannel-docker:network', 'docker:network')

        try:
            cls.deployment.setup(timeout=seconds)
            cls.deployment.sentry.wait()
        except amulet.helpers.TimeoutError:
            msg = "The environment was not set up in %d seconds." % seconds
            amulet.raise_status(amulet.FAIL, msg)
        except:
            raise

        cls.docker_unit = cls.deployment.sentry.unit['docker/0']
        cls.etcd_unit = cls.deployment.sentry.unit['etcd/0']

    def test_flannel_binary(self):
        """ Test to see if flannel is installed correctly. """
        command = 'flannel --version'
        # Run the command to see if flannel is installed on the docker unit.
        output, code = self.docker_unit.run(command)
        print(command, output)
        if code != 0:
            message = 'The flannel binary is not installed.'
            amulet.raise_status(amulet.FAIL, msg=message)

    def test_flannel_running(self):
        """ Test to see if flannel is running correctly. """
        command = 'sudo service flannel status'
        # Run the command to see if flannel is running on the docker unit.
        output, code = self.docker_unit.run(command)
        print(command, output)
        if code != 0:
            message = 'The flannel process is not in correct status.'
            amulet.raise_status(amulet.FAIL, msg=message)

    def test_flannel_config(self):
        """ Test the flannel configuration. """
        flannel_config_file = '/etc/init/flannel.conf'
        # Get the flannel configuration file on the docker unit.
        flannel_config = self.docker_unit.file_contents(flannel_config_file)
        etcd_public_address = self.etcd_unit.info['public-address']
        print('etcd public address:', etcd_public_address)
        # Must get the etcd relation to get the relation information.
        etcd_relation = self.etcd_unit.relation('client', 'flannel-docker:db')
        etcd_private_address = etcd_relation['private-address']
        print('etcd private address:', etcd_private_address)
        etcd_port = etcd_relation['port']
        print('etcd port:', etcd_port)
        # Search the configuration for the etcd private address.
        address_index = flannel_config.find(etcd_private_address)
        # Search the configuration for the etcd port.
        port_index = flannel_config.find(etcd_port)
        found_address = address_index != -1
        found_port = port_index != -1
        if found_address and found_port:
            print('The flannel configuration had correct etcd information.')
        else:
            print(flannel_config)
            message = 'Flannel did not have the correct etcd information.'
            amulet.raise_status(amulet.FAIL, msg=message)


if __name__ == '__main__':
    unittest.main()
