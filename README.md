# duffel

Python client library for the [Duffel API](https://duffel.com/docs/api).

## Requirements

- Python 3.6+

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

api_token = 'test_...'
client = Duffel(api_token = api_token)
```

After you have a client you can interact with, you can make calls to the Duffel API:

```python
from duffel_api import Duffel

client = Duffel(api_token = 'test...')

offer_requests = client.offer_requests.list()
for offer_request in offer_requests:
    print(offer_request.id)
```

You can find a complete example of booking a flight in [./examples/book-flight.py](./examples/book-flight.py).

## Development

Run all the tests:
```bash
tox
```

As part of running `tox`, a code coverage report is built for you. You can navigate it by opening `htmlcov/index.html`
in a browser, or if in a OS that supports it by using `open` (alternative `xdg-open`):

```bash
open ./htmlcov/index.html
```
