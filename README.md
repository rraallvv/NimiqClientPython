# Nimiq Client Python

A simple python client for the [Nimiq](http://nimiq.com/) JSON RPC API.

## Install

### From GIT

```
$ git clone https://github.com/rraallvv/NimiqClientPython
$ cd NimiqClientPython
$ python3 setup.py install
```

## Usage

1. `import nimiqclient`
1. `nimiq = NimiqClient()` or `NimiqClient(scheme = "http", user = "luna", password = "moon", host = "127.0.0.1", port = 8648)`
1. Do whatever you like, e.g. get the genesis block: `nimiq.getBlockByNumber(0)`
