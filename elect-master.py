#!/usr/bin/python

import os
import sys
import argparse
import requests
import urlparse
import socket

default_etcd_server = 'http://localhost:4001'

def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument('--server', '-s',
                   default=default_etcd_server)
    p.add_argument('key')
    return p.parse_args()


def get_my_ip(server):
    url = urlparse.urlparse(server)

    try:
        host, port = url.netloc.split(':')
    except ValueError:
        host = url.netloc
        port = 80

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, int(port)))

    try:
        return s.getpeername()
    finally:
        s.close()


def register_key(server, key, id):
    res = requests.put(
        '%s/v2/keys/%s?prevExist=false' % (server, key),
        params={'value': id})
    res.raise_for_status()


def get_key_value(server, key):
    res = requests.get(
        '%s/v2/keys/%s' % (server, key))
    res.raise_for_status()
    res = res.json()
    return res['node']['value']


def main():
    retval = 0
    args = parse_args()

    if args.server.endswith('/'):
        args.server = args.server[:-1]
    if args.key.startswith('/'):
        args.key = args.key[1:]

    myid = get_my_ip(args.server)

    try:
        register_key(args.server, args.key, myid)
    except requests.HTTPError as err:
        if err.response.status_code != 412:
            raise
        retval = 10

    master = get_key_value(args.server, args.key)
    print master
    sys.exit(retval)


if __name__ == '__main__':
    main()

