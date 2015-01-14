---
layout: default
title: Relations and Interfaces
category: User Docs
permalink: /user/relations-and-interfaces.html
---

# Configuration Through Relations

## Exposed Interfaces

#### Relationship: Network

##### Interface: overlay-network

##### scope: container

**Sends Variables**

- flannel-subnet
- flannel-mtu


The network relationship joins the flannel-docker service and a consuming charm, such as the [Docker](http://github.com/chuckbutler/docker-charm/) Charm, who receives the subnet and mtu - and configures it's virtual ethernet device accordingly.



## Consumed Interfaces

#### Relationship: docker-host

##### Scope: container

##### Interface: juju-info

This relationship is used to actually deploy the Subordinate unit on to the Juju Charm. Interfaces that consume `juju-info` are special cases and reserved by Juju. More on this in the [Subordinate Services](https://jujucharms.com/docs/authors-subordinate-services) Documentation.


#### Relationship: DB

##### Interface: etcd

**Receives Variables**

- port
- private-address

Responsible for communicating with the ETCD server to register itself and receive data back to configure the host subnet for the virtual ethernet adapter. Also configures the Flannel Service, starts the Flannel Daemon, and relay's the subnet data through the [network](http://localhost:4000/user/relations-and-interfaces.html#relationship-network) relation.



## Peering Interfaces

#### Relationship: overlay

##### interface: flannel-mesh

> Not currently Implemented
