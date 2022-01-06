[![PyPI](https://img.shields.io/pypi/v/duffel-api?style=flat-square)](https://pypi.org/project/duffel-api/)
[![Supported Python
versions](https://img.shields.io/pypi/pyversions/duffel-api.svg)](https://pypi.org/project/duffel-api/)
[![Build Status](https://github.com/duffelhq/duffel-api-python/actions/workflows/main.yaml/badge.svg)](https://github.com/duffelhq/duffel-api-python/actions/workflows/main.yaml)
[![Code style:black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Downloads](https://pepy.tech/badge/duffel-api/month)](https://pepy.tech/project/duffel-api/month)

# duffel-api

Python client library for the [Duffel API](https://duffel.com/docs/api).

## Requirements

- Python 3.7+

## Getting started

```shell
pip install duffel-api
```

## Usage

You first need to set the API token you can find in the Duffel [dashboard](https://app.duffel.com) under the section
Developers > Access Tokens.

Once you have the token, you can call `Duffel()` with the value:

```python
from duffel_api import Duffel

access_token = 'test_...'
client = Duffel(access_token = access_token)
```

After you have a client you can interact with, you can make calls to the Duffel API:

```python
from duffel_api import Duffel

client = Duffel(access_token = 'test...')

offer_requests = client.offer_requests.list()
for offer_request in offer_requests:
    print(offer_request.id)
```

You can find a complete example of booking a flight in [./examples/book-flight.py](./examples/book-flight.py).

## Development

### Testing

Run all the tests:

```bash
tox
```

As part of running `tox`, a code coverage report is built for you. You can navigate it by opening `htmlcov/index.html`
in a browser, or if in a OS that supports it by using `open` (alternative `xdg-open`):

```bash
open ./htmlcov/index.html
```

### Packaging

Setup pypi config (`~/.pypirc`):
```text
[pypi]
  username = __token__
  password = pypi-generated-token

[testpypi]
  username = __token__
  password = pypi-generated-token
```

Install dependencies:
```bash
pip install wheel twine
```

Build the package before uploading:

```bash
python setup.py sdist bdist_wheel
```

Upload packages (test):

```bash
twine upload -r testpypi --verbose dist/*
```

The above will upload the packages to [test.pypi.org](https://test.pypi.org) which will allow you to verify all is well
with your upload before uploading it to the main pypi repository.

```bash
twine upload -r pypi --verbose dist/*
```
