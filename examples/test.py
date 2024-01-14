"""Basic example for TradierRestAdapter."""

import json
import aiohttp
import asyncio
import datetime
import logging


from aiotradier import TradierAPIAdapter, TradierError


_LOGGER = logging.getLogger("aiotradier.tradier_rest")


async def do_account_stuff(client):
    """Exercise API functions related to accounts."""

    res = await client.api_get_user_profile()
    account_id = res["profile"]["account"]["account_number"]

    # three requests going out
    await asyncio.gather(
        client.api_get_balances(account_id),
        client.api_get_positions(account_id),
        client.api_get_account_history(account_id),
    )


async def do_market_stuff(client):
    """Exercise API functions to get information about securities."""

    symbol = "M"

    res = await client.api_get_quotes([symbol], False)

    res = await client.api_get_option_expirations(symbol, include_all_roots=False)
    next_expiration = res["expirations"]["date"][0]
    next_expiration = datetime.datetime.strptime(next_expiration, "%Y-%m-%d")
    await client.api_get_option_strikes("M", next_expiration)
    await client.api_get_option_chains(symbol, next_expiration)

    await client.api_get_historical_quotes(
        symbol,
        start=datetime.date(year=2024, month=1, day=1),
        end=datetime.date(year=2024, month=1, day=9),
    )

    await client.api_get_timesales(
        symbol,
        start=datetime.datetime(year=2024, month=1, day=1, hour=10, minute=0),
        end=datetime.datetime(year=2024, month=1, day=1, hour=10, minute=35),
        interval="5min",
    )

    await client.api_get_clock()
    await client.api_get_search("alphabet")
    await client.api_get_lookup(
        "goog", exchanges=["Q", "N"], types=["stock", "option", "etf", "index"]
    )


async def do_fundamentals_stuff(client):
    """Exercise API functions about Fundamentals."""

    symbols = ["M"]
    await client.api_get_dividends(symbols)
    await client.api_get_calendars(symbols)


async def main():
    """Run Tradier get info example."""

    _LOGGER.setLevel(20)  # set to 10 to see requests/responses
    _LOGGER.addHandler(logging.StreamHandler())

    with open("token.txt", "r", encoding="utf-8") as file:
        token = file.readline().strip()

    async with aiohttp.ClientSession() as aiohttp_session:
        client = TradierAPIAdapter(aiohttp_session, token)

        try:
            await do_account_stuff(client)
            await do_market_stuff(client)
            await do_fundamentals_stuff(client)

        except TradierError as err:
            print(f"Error: {err.args}")

    with open("data.txt", mode="w", encoding="utf-8") as file:
        file.write(json.dumps(client.raw_data(), indent=4))


if __name__ == "__main__":
    asyncio.run(main())
