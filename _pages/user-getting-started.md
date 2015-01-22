---
layout: default
title: Getting Started
category: User Docs
permalink: /user/getting-started.html
---

# Deploy the Docker Runtime

See the Excellent [Getting Started](http://chuckbutler.github.io/docker-charm/user/getting-started.html#deploying-the-stable-charm) Docs maintained by the docker-charm repository to get up to speed with deploying docker.

# Deploy the Flannel Docker Charm

## Deploying the Stable Charm

> The flannel-docker charm is not presently in the charm store. These instructions being applicable are pending a full charm review and acceptance to the charm-store. This warning will be removed upon promulgation of the charm.

    juju deploy cs:~hazmat/trusty/etcd
    juju deploy cs:trusty/flannel-docker
    juju add-relation flannel-docker:docker-host docker:juju-info
    juju add-relation flannel-docker:network docker:network
    juju add-relation etcd:client flannel-docker:db


## Deploying the Development Charm

> **Warning:** Deploying the Development Focus is not guaranteed to be stable - and not recommended for production deployments!

The Flannel-Docker charm will be in varying states in the master branch of it’s github repository. We attempt to follow [Semantic Versioning](http://semver.org) as closely as we can - to tag the snapshots of the charm in specifics states of evolution. *This will not resemble the versioning in the juju charm store.*

    mkdir -p ~/charms/trusty
    export JUJU_REPOSITORY=$HOME/charms
    git clone https://github.com/chuckbutler/docker-charm.git ~/charms/trusty/docker
    git clone https://github.com/chuckbutler/flannel-docker-charm.git ~/charms/trusty/flannel-docker
    juju deploy local:trusty/docker
    juju deploy local:trusty/flannel-docker
    juju deploy cs:~hazmat/trusty/etcd
    juju add-relation etcd:client flannel-docker:db
    juju add-relation flannel-docker:docker-host docker:juju-info
    juju add-relation flannel-docker:network docker:network


# Known Limitations

### Local Provider Blockers

The Flannel-Docker Charm will not work out of the box on the local provider. LXC containers are goverend by a very strict App Armor policy that prevents accidental misuses of privilege inside the container. Thus **running the Flannel-Docker Charm inside the local provider is not a supported deployment method.**

### Non X86 Support

The current shipping version of Flannel-Docker contains a compiled binary that is self sufficent on X86 hosts. This will not work on ARM64 or PPC64EL hosts that we are aware of. If you're interested in contributing a binary to enable these platforms - see our [Contributing]({{ site.url }}/dev/contributing.html) Docs.
