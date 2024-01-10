"""Basic example for TradierRestAdapter."""


import asyncio
import datetime
import logging
import sys

import aiohttp

sys.path.insert(0, "/home/vscode/aiotradier/")
from aiotradier.tradier_rest import TradierAPIAdapter
from aiotradier.exceptions import TradierError


_LOGGER = logging.getLogger("aiotradier.tradier_rest")


async def do_account_stuff(client):
    """Exercise API functions related to accounts."""
    res = await client.api_get_user_profile()
    print(res)
    account_id = res["profile"]["account"]["account_number"]

    res = await client.api_get_balances(account_id)
    print(res)

    res = await client.api_get_positions(account_id)
    print(res)

    res = await client.api_get_account_history(account_id)
    print(res)


async def do_quotes_stuff(client):
    """Exercise API functions to get information about securities."""
    res = await client.api_get_quotes(["M", "T"], False)
    print(res)

    symbol = "M"
    res = await client.api_get_option_expirations(symbol, include_all_roots=False)
    print(res)

    next_expiration = res["expirations"]["date"][0]
    next_expiration = datetime.datetime.strptime(next_expiration, "%Y-%m-%d")
    res = await client.api_get_option_strikes("M", next_expiration)
    print(res)

    # res = await client.api_get_option_chains(symbol, next_expiration)
    # print(res)

    res = await client.api_get_historical_quotes(
        symbol,
        start=datetime.date(year=2024, month=1, day=1),
        end=datetime.date(year=2024, month=1, day=9),
    )
    print(res)

    res = await client.api_get_clock()
    print(res)


async def main():
    """Run Tradier get info example."""

    _LOGGER.setLevel(10)
    _LOGGER.addHandler(logging.StreamHandler())

    with open("token.txt", "r", encoding="utf-8") as file:
        token = file.readline().strip()

    async with aiohttp.ClientSession() as aiohttp_session:
        client = TradierAPIAdapter(aiohttp_session, token)

        try:
            await do_account_stuff(client)
            await do_quotes_stuff(client)

        except TradierError as err:
            print(f"Error: {err.args}")

    # print(client.raw_data())


if __name__ == "__main__":
    asyncio.run(main())
