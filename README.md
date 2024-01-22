## aiotradier

Python library to access Tradier´s API using Async IO

Tradier's documentation is at https://documentation.tradier.com/brokerage-api

This is a very lightweight library to wrap Tradier's API. It implements functions to access most of
the endpoints for Accounts, Market Data, and Trading. It does not include yet functions to access Authentication or Watchlists.
Instead of authenticating with the API, you can obtain a token by logging into your account. 

## Requirements

- Python >= 3.11

## Install

```bash
pip install aioatradier
```

## Install from Source

Run the following command inside this folder

```bash
pip install --upgrade .
```

## Examples

Examples can be found in the `examples` folder
