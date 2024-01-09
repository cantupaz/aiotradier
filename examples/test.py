"""Basic example for TradierRestAdapter."""


import asyncio
import datetime
import logging
import sys

import aiohttp

sys.path.insert(0, "/home/vscode/OptionScreener/OptionScreener/aiotradier/")
from aiotradier.tradier_rest import TradierRestAdapter
from aiotradier.exceptions import TradierError


_LOGGER = logging.getLogger(__name__)

token = ""


async def do_account_stuff(client):
    """Exercise some API functions."""
    res = await client.api_get_user_profile()
    print(res)
    account_id = res["profile"]["account"]["account_number"]

    res = await client.api_get_balances(account_id)
    print(res)

    res = await client.api_get_positions(account_id)
    print(res)


async def do_quotes_stuff(client):
    res = await client.api_get_quotes(["M", "T"], False)
    print(res)

    symbol = "M"
    res = await client.api_get_option_expirations(symbol, include_all_roots=False)
    print(res)

    next_expiration = res["expirations"]["date"][0]
    next_expiration = datetime.datetime.strptime(next_expiration, "%Y-%m-%d")
    res = await client.api_get_option_strikes("M", next_expiration)
    print(res)

    res = await client.api_get_option_chains(symbol, next_expiration)
    print(res)


async def main():
    """Run Tradier get info example."""

    _LOGGER.setLevel(10)
    _LOGGER.addHandler(logging.StreamHandler())

    async with aiohttp.ClientSession() as aiohttp_session:
        client = TradierRestAdapter(aiohttp_session, token)

        try:
            # await do_account_stuff(client)
            await do_quotes_stuff(client)

        except TradierError as err:
            print(f"Error: {err.args}")

    print(client.raw_data())


if __name__ == "__main__":
    asyncio.run(main())
