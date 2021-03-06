Nimiq Client Python
===================

[![build](https://github.com/rraallvv/NimiqClientPython/workflows/build/badge.svg)](https://github.com/rraallvv/NimiqClientPython/actions)
[![PyPI version](https://badge.fury.io/py/nimiqclient.svg)](https://pypi.org/project/nimiqclient)
[![Maintainability](https://api.codeclimate.com/v1/badges/b539d9690dc040c3f33d/maintainability)](https://codeclimate.com/github/rraallvv/NimiqClientPython/maintainability)
[![Coverage Status](https://coveralls.io/repos/github/rraallvv/NimiqClientPython/badge.svg?branch=master)](https://coveralls.io/github/rraallvv/NimiqClientPython?branch=master)

> Python implementation of the Nimiq RPC client specs.

## Usage

Send requests to a Nimiq node with `NimiqClient` object.

```python
client = NimiqClient(
    scheme = "http",
    host = "127.0.0.1",
    port = 8648,
    user = "luna",
    password = "moon"
)
```
Once the client have been set up, we can call the methodes with the appropiate arguments to make requests to the Nimiq node.

When no configuration is passed in the initialization it will use defaults for the Nimiq node.

```python
client = NimiqClient()

# make rpc call to get the block number
blockNumber = client.blockNumber()

print(blockNumber) # displays the block number, for example 748883
```

## API

The complete [API documentation](docs) is available in the `/docs` folder.

Check out the [Nimiq RPC specs](https://github.com/nimiq/core-js/wiki/JSON-RPC-API) for behind the scene RPC calls.

## Installation

The recommended way to install Nimiq Python Client is via a Python package manager like pip.

## Contributions

This implementation was originally contributed by [rraallvv](https://github.com/rraallvv/).

Please send your contributions as pull requests.

Refer to the [issue tracker](https://github.com/rraallvv/NimiqClientPython/issues) for ideas.

### Develop

After cloning the repository intall the package.

```
$ git clone https://github.com/rraallvv/NimiqClientPython
$ cd NimiqClientPython
$ python setup.py install
```

All done, happy coding!

### Testing

Tests are stored in the `/tests` folder and can be run with the script `test.py`.

```
$ python -m unittest discover -v
```

### Documentation

The documentation is generated automatically by running [Doxygen](https://www.doxygen.nl/download.html#srcbin) from the repository root directory.

```
doxygen doxygenfile
```

## License

[MIT](LICENSE)
