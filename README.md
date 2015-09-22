# Flannel (Docker Flavored)

[![Build Status](http://drone.systemzoo.org/api/badge/github.com/chuckbutler/flannel-docker-charm/status.svg?branch=master)](http://drone.systemzoo.org/github.com/chuckbutler/flannel-docker-charm)

### About Flannel
[Flannel](https://github.com/coreos/flannel) (originally rudder) is an overlay
network that gives a subnet to each machine for use with containers.

One of the common issues when using containers in clouds is the inability to do cross
host communication between the containers as they default to using a local bridge.

flannel uses the Universal TUN/TAP device and creates an overlay network using UDP to
encapsulate IP packets. The subnet allocation is done with the help of etcd which maintains
the overlay subnet to host mappings.

This charm uses flannel to setup an overlay network and configures docker containers
on that host to use the overlay.

> **NOTE!** For up to date, and complete documentation - please see the [Charm Documentation](http://chuckbutler.github.io/flannel-docker-charm/) Site.

## Charm Usage

Flannel-docker is a subordinate charm, and is designed to be be deployed into the scope of
a docker host, configuring its networking bridge (docker0) to use the TUN/TAP overlay
network so docker containers can communicate cross-host. This facilitates in HA and colocated
networking deployment.

#### Deployment

Start by deploying ETCD to your bootstrap node (this is for cost reduction, its not uncommon for multiple etcd hosts to reside as a cluster for HA scenarios. This particular deployment is non-HA)

Deploy the docker charm, and flannel-docker. Then relate docker to flannel-docker, and flannel-docker to etcd. The networking magic will reconfigure the network as a mesh overlay.

    juju deploy cs:~kubernetes/trusty/etcd --to 0
    juju deploy trusty/docker
    juju deploy trusty/flannel-docker
    juju add-relation flannel-docker:docker-host docker:juju-info
    juju add-relation flannel-docker:db etcd:client
    juju add-relation flannel-docker:network docker:network

## Known Limitations

This charm does not currently work with the Juju local provider. The combination
of apparmor and LXC prevent the flannel function from working.  Deploy this
charm to a cloud environment.

The included binary files are amd64 only. The flannel code is compiled and will
not run on architectures other than amd64 (x86_64).  Use the `constraints` flag
with the `juju` command to specify the proper architecture from your cloud environment.

# Contact information

The Flannel-Docker subordinate is heavily based on the Flannel charm produced by Kapil Thangavelu

- Maintainer: Charles Butler &lt;charles.butler@ubuntu.com&gt;

## Flannel information

- [Flannel on GitHub](https://github.com/coreos/flannel)
- [Charm Issue Tracker](https://github.com/chuckbutler/flannel-docker-charm/issues)
- [Charm Documentation](http://chuckbutler.github.io/flannel-docker-charm/)
