#!/usr/bin/env python

import urllib
import urlparse
import json
import httplib
import argparse
import subprocess
import sys


def initialize_etcd(endpoint,
                    flannel_prefix="/coreos.com/network",
                    flannel_network="10.10.0.0/16"):
    try:
        parsed = urlparse.urlparse(endpoint)
        params = urllib.urlencode(
            {"value": json.dumps({'Network': flannel_network})})
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        path = "/v2/keys%s/config" % flannel_prefix
        conn = httplib.HTTPConnection(parsed.hostname, parsed.port)
        conn.request("PUT", path, params, headers)
        response = conn.getresponse()
        data = json.loads(response.read())
        print("Initialize Etcd Network %s %s" % (response.status,
                                                 response.reason))
        print(data)
    except:
        msg = "Unable to register with ETCD. Flannel not configured"
        cmd = ['status-set', 'blocked', msg]
        subprocess.call(cmd)
        return 0


def main(args=sys.argv[1:]):
    parser = argparse.ArgumentParser(description="stuff")
    parser.add_argument("endpoint")
    args = parser.parse_args(args)
    initialize_etcd(args.endpoint)


if __name__ == "__main__":
    main()
