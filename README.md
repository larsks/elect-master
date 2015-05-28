Simple master election using [etcd][].

## Synopsis

    elect-master [-s server] key

## Description

This script will attempt to atomically register the given key with
etcd.  It will set the value of the key to the ip address of the local
client (as determined by opening a connection to the etcd server and
then calling `getpeername()`).

If `elect-master` is able to register the key, it will print the
registered ip address and return 0.

If `elect-master` is unable to register the key because the key
already exists, it will print the value of the key and return 10.

If `elect-master` is unable to register the key for any other reason,
it will return 1.

[etcd]: https://coreos.com/etcd/
