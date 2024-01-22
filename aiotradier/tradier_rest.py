"""Provide AsyncIO access to Tradier API"""

import logging
from datetime import date, datetime
import json
from typing import Any, cast
from aiohttp import ClientConnectorError, ClientResponseError, ClientSession


from .common import (
    EquityOrderSide,
    OptionOrderSide,
    OrderClass,
    OrderDuration,
    OrderType,
    SortBy,
    SortOrder,
)
from .exceptions import TradierError, APIError, AuthError
from .const import (
    API_ACCOUNTS,
    API_BALANCES,
    API_BETA,
    API_CALENDAR,
    API_CALENDARS,
    API_CHAINS,
    API_CLOCK,
    API_COMPANY,
    API_DIVIDENDS,
    API_EXPIRATIONS,
    API_FUNDAMENTALS,
    API_GAINLOSS,
    API_HISTORY,
    API_LOOKUP,
    API_MARKETS,
    API_OPTIONS,
    API_ORDERS,
    API_POSITIONS,
    API_PROFILE,
    API_QUOTES,
    API_SANDBOX_URL,
    API_SEARCH,
    API_STRIKES,
    API_TIMESALES,
    API_URL,
    API_USER,
    API_V1,
    HTTP_CALL_TIMEOUT,
    RAW_ACCOUNT_HISTORY,
    RAW_BALANCES,
    RAW_CALENDAR,
    RAW_CALENDARS,
    RAW_CHAINS,
    RAW_CLOCK,
    RAW_COMPANY,
    RAW_DIVIDENDS,
    RAW_EXPIRATIONS,
    RAW_GAINLOSS,
    RAW_HISTORICAL_QUOTES,
    RAW_LOOKUP,
    RAW_ORDER_DETAIL,
    RAW_ORDERS,
    RAW_PLACE_EQUITY_ORDER,
    RAW_PLACE_OPTION_ORDER,
    RAW_POSITIONS,
    RAW_SEARCH,
    RAW_STRIKES,
    RAW_TIMESALES,
    RAW_USER_PROFILE,
    RAW_QUOTES,
)

_LOGGER = logging.getLogger(__name__)


class TradierAPIAdapter:
    """Access Tradier API."""

    def __init__(
        self, aiohttp_session: ClientSession | None, token: str = "", sandbox=True
    ):
        """Set up the Adapter."""

        self.aiohttp_session: ClientSession | None = aiohttp_session
        self.token = token
        self.url = API_SANDBOX_URL if sandbox else API_URL

        self._api_raw_data: dict[str, Any] = {}

    async def _api_request(
        self,
        method: str,
        path: str,
        payload: Any | None = None,
        params: Any | None = None,
    ) -> dict[str, Any]:
        """Tradier API request."""

        full_url = f"{self.url}/{path}"

        if self.aiohttp_session is None:
            aiohttp_session = ClientSession()
        else:
            aiohttp_session = self.aiohttp_session

        headers = {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/json",
        }

        _LOGGER.debug(
            "aiohttp request: %s %s (params=%s) (headers=%s) (payload=%s)",
            method,
            full_url,
            params,
            headers,
            payload,
        )

        try:
            async with aiohttp_session.request(
                method,
                full_url,
                headers=headers,
                json=payload,
                params=params,
                raise_for_status=True,
                timeout=HTTP_CALL_TIMEOUT,
            ) as resp:
                resp_text = await resp.text()
        except ClientConnectorError as err:
            raise TradierError(err) from err
        except ClientResponseError as err:
            if err.status == 400:
                raise APIError(err) from err
            if err.status == 401:
                raise AuthError(err) from err
            raise TradierError(err) from err

        finally:
            if self.aiohttp_session is None:
                await aiohttp_session.close()

        try:
            resp_json = json.loads(resp_text)
        except json.JSONDecodeError as err:
            _LOGGER.error("Problems decoding response %s", resp_text)
            raise TradierError(err) from err

        _LOGGER.debug("aiohttp response: %s", resp_json)
        return cast(dict[str, Any], resp_json)

    ############ Account

    async def api_get_user_profile(self) -> dict[str, Any]:
        "Get user profile (includes account metadata)."
        res = await self._api_request(
            "GET",
            f"{API_V1}/{API_USER}/{API_PROFILE}",
        )
        self._api_raw_data[RAW_USER_PROFILE] = res

        return res

    async def api_get_balances(self, account_id: str) -> dict[str, Any]:
        """Get account balances."""
        res = await self._api_request(
            "GET", f"{API_V1}/{API_ACCOUNTS}/{account_id}/{API_BALANCES}"
        )
        self._api_raw_data[RAW_BALANCES] = res

        return res

    async def api_get_positions(self, account_id: str) -> dict[str, Any]:
        """Get account positions."""
        res = await self._api_request(
            "GET", f"{API_V1}/{API_ACCOUNTS}/{account_id}/{API_POSITIONS}"
        )
        self._api_raw_data[RAW_POSITIONS] = res

        return res

    async def api_get_account_history(
        self,
        account_id: str,
        page: int | None = None,
        limit: int | None = None,
        type_: str | None = None,
        start: date | None = None,
        end: date | None = None,
        symbol: str | None = None,
        exact_match: bool = False,
    ) -> dict[str, Any]:
        """Get account history."""

        params = {
            "account_id": account_id,
        }
        if page:
            params["page"] = "f{page}"
        if limit:
            params["limit"] = f"{limit}"
        if type_:
            params["type_"] = f"{type_}"
        if start:
            params["start"] = start.strftime("%Y-%m-%d")
        if end:
            params["end"] = end.strftime("%Y-%m-%d")
        if symbol:
            params["symbol"] = symbol
        if exact_match:
            params["exact_match"] = f"{exact_match}"

        res = await self._api_request(
            "GET", f"{API_V1}/{API_ACCOUNTS}/{account_id}/{API_HISTORY}", params=params
        )
        self._api_raw_data[RAW_ACCOUNT_HISTORY] = res

        return res

    async def api_get_account_gainloss(
        self,
        account_id: str,
        page: int | None = None,
        limit: int | None = None,
        sort_by: SortBy | None = None,
        sort_order: SortOrder | None = None,
        start: date | None = None,
        end: date | None = None,
        symbol: str | None = None,
        exact_match: bool = False,
    ) -> dict[str, Any]:
        """Get account history."""

        params = {
            "account_id": account_id,
        }
        if page:
            params["page"] = "f{page}"
        if limit:
            params["limit"] = f"{limit}"
        if sort_by:
            params["sortBy"] = str(sort_by)
        if sort_order:
            params["sort"] = str(sort_order)
        if start:
            params["start"] = start.strftime("%Y-%m-%d")
        if end:
            params["end"] = end.strftime("%Y-%m-%d")
        if symbol:
            params["symbol"] = symbol

        res = await self._api_request(
            "GET", f"{API_V1}/{API_ACCOUNTS}/{account_id}/{API_GAINLOSS}", params=params
        )
        self._api_raw_data[RAW_GAINLOSS] = res

        return res

    async def api_get_account_orders(
        self,
        account_id: str,
        page: int | None = None,
        include_tags: bool | None = None,
    ) -> dict[str, Any]:
        """Retrieve orders placed within an account.
        This API will return orders placed for the market session of the present calendar day."""

        params = {"account_id": account_id}

        if page:
            params["page"] = "f{page}"
        if include_tags:
            params["includeTags"] = str(include_tags)

        res = await self._api_request(
            "GET", f"{API_V1}/{API_ACCOUNTS}/{account_id}/{API_ORDERS}", params=params
        )
        self._api_raw_data[RAW_ORDERS] = res

        return res

    async def api_get_order(
        self,
        account_id: str,
        order_id: str,
        include_tags: bool | None = None,
    ) -> dict[str, Any]:
        """Get detailed information about a previously placed order."""

        params = {"account_id": account_id}

        if include_tags:
            params["includeTags"] = str(include_tags)

        res = await self._api_request(
            "GET",
            f"{API_V1}/{API_ACCOUNTS}/{account_id}/{API_ORDERS}/{order_id}",
            params=params,
        )
        self._api_raw_data[RAW_ORDER_DETAIL] = res

        return res

    ############# Market Data

    async def api_get_quotes(
        self, symbols: list[str], greeks: bool = False
    ) -> dict[str, Any]:
        """Get a list of symbols using a keyword lookup on the symbols description.
        Results are in descending order by average volume of the security."""

        params = {"symbols": ",".join(symbols), "greeks": f"{greeks}"}
        res = await self._api_request(
            "GET", f"{API_V1}/{API_MARKETS}/{API_QUOTES}", params=params
        )
        self._api_raw_data[RAW_QUOTES] = res

        return res

    async def api_get_option_expirations(
        self,
        symbol: str,
        include_all_roots: bool = False,
        strikes: bool = False,
        contract_size: bool = False,
        expiration_type: bool = False,
    ) -> dict[str, Any]:
        """Get expiration dates for a particular underlying."""

        params = {
            "symbol": symbol,
            "includeAllRoots": f"{include_all_roots}",
            "strikes": f"{strikes}",
            "contractSize": f"{contract_size}",
            "expirationType": f"{expiration_type}",
        }
        res = await self._api_request(
            "GET",
            f"{API_V1}/{API_MARKETS}/{API_OPTIONS}/{API_EXPIRATIONS}",
            params=params,
        )
        self._api_raw_data[RAW_EXPIRATIONS] = res

        return res

    async def api_get_option_strikes(
        self,
        symbol: str,
        expiration: date,
    ) -> dict[str, Any]:
        """Get an options strike prices for a specified expiration date."""

        params = {
            "symbol": symbol,
            "expiration": expiration.strftime("%Y-%m-%d"),
        }
        res = await self._api_request(
            "GET", f"{API_V1}/{API_MARKETS}/{API_OPTIONS}/{API_STRIKES}", params=params
        )
        self._api_raw_data[RAW_STRIKES] = res

        return res

    async def api_get_option_chains(
        self, symbol: str, expiration: date, greeks: bool = False
    ) -> dict[str, Any]:
        """Get all quotes in an option chain."""
        params = {
            "symbol": symbol,
            "expiration": expiration.strftime("%Y-%m-%d"),
            "greeks": f"{greeks}",
        }
        res = await self._api_request(
            "GET", f"{API_V1}/{API_MARKETS}/{API_OPTIONS}/{API_CHAINS}", params=params
        )
        self._api_raw_data[RAW_CHAINS] = res

        return res

    async def api_get_historical_quotes(
        self,
        symbol: str,
        interval: str | None = None,
        start: date = None,
        end: date = None,
        session_filter: str = None,
    ) -> dict[str, Any]:
        """Get historical pricing for a security.
        This data will usually cover the entire lifetime of the company if sending
        reasonable start/end times. You can fetch historical pricing for options
        by passing the OCC option symbol (ex. AAPL220617C00270000) as the symbol."""

        params = {"symbol": symbol}
        if interval:
            params["interval"] = f"{interval}"
        if start:
            params["start"] = start.strftime("%Y-%m-%d")
        if end:
            params["end"] = end.strftime("%Y-%m-%d")
        if session_filter:
            params["session_filter"] = f"{session_filter}"

        res = await self._api_request(
            "GET", f"{API_V1}/{API_MARKETS}/{API_HISTORY}", params=params
        )
        self._api_raw_data[RAW_HISTORICAL_QUOTES] = res

        return res

    async def api_get_timesales(
        self,
        symbol: str,
        interval: str | None = "tick",
        start: datetime = None,
        end: datetime = None,
        session_filter: str = None,
    ) -> dict[str, Any]:
        """Time and Sales (timesales) is typically used for charting purposes.
        It captures pricing across a time slice at predefined intervals.
        Tick data is also available through this endpoint. This results in a very large
        data set for high-volume symbols, so the time slice needs to be much smaller
        to keep downloads time reasonable."""

        params = {"symbol": symbol}
        if interval:
            params["interval"] = f"{interval}"
        if start:
            params["start"] = start.strftime("%Y-%m-%d %H:%M")
        if end:
            params["end"] = end.strftime("%Y-%m-%d %H:%M")
        if session_filter:
            params["session_filter"] = f"{session_filter}"

        res = await self._api_request(
            "GET", f"{API_V1}/{API_MARKETS}/{API_TIMESALES}", params=params
        )
        self._api_raw_data[RAW_TIMESALES] = res

        return res

    async def api_get_clock(self, delayed: bool = False) -> dict[str, Any]:
        """Get the intraday market status.
        This call will change and return information pertaining to the current
        day. If programming logic on whether the market is open/closed – this
        API call should be used to determine the current state."""

        params = {"delayed": f"{delayed}"}
        res = await self._api_request(
            "GET", f"{API_V1}/{API_MARKETS}/{API_CLOCK}", params=params
        )
        self._api_raw_data[RAW_CLOCK] = res

        return res

    async def api_get_calendar(
        self, month: int | None = None, year: int | None = None
    ) -> dict[str, Any]:
        """Get the market calendar for the current or given month.
        This can be used to plan ahead regarding strategies.
        However, api_get_clock should be used to determine the current status of the market.
        """
        params = {
            "month": f"{month:2f}",
            "year": f"{year}",
        }
        res = await self._api_request(
            "GET", f"{API_V1}/{API_MARKETS}/{API_CALENDAR}", params=params
        )
        self._api_raw_data[RAW_CALENDAR] = res

        return res

    async def api_get_search(self, query: str) -> dict[str, Any]:
        """Get a list of symbols using a keyword lookup on the symbols description.
        Results are in descending order by average volume of the security.
        This can be used for simple search functions."""

        params = {"q": query}
        res = await self._api_request(
            "GET", f"{API_V1}/{API_MARKETS}/{API_SEARCH}", params=params
        )
        self._api_raw_data[RAW_SEARCH] = res

        return res

    async def api_get_lookup(
        self,
        query: str,
        exchanges: list[str] | None = None,
        types: list[str] | None = None,
    ) -> dict[str, Any]:
        """Search for a symbol using the ticker symbol or partial symbol.
        Results are in descending order by average volume of the security.
        This can be used for simple search functions."""

        params = {"q": query}
        if exchanges:
            params["exchanges"] = ",".join(exchanges)
        if types:
            params["types"] = ",".join(types)

        res = await self._api_request(
            "GET", f"{API_V1}/{API_MARKETS}/{API_LOOKUP}", params=params
        )
        self._api_raw_data[RAW_LOOKUP] = res

        return res

    ############# Fundamentals

    async def api_get_company(self, symbols: list[str]) -> dict[str, Any]:
        """Get company fundamental information."""
        params = {"symbols": ",".join(symbols)}
        res = await self._api_request(
            "GET",
            f"{API_BETA}/{API_MARKETS}/{API_FUNDAMENTALS}/{API_COMPANY}",
            params=params,
        )
        self._api_raw_data[RAW_COMPANY] = res

    async def api_get_calendars(self, symbols: list[str]) -> dict[str, Any]:
        """Get corporate calendar information for securities.
        This does not include dividend information."""

        params = {"symbols": ",".join(symbols)}
        res = await self._api_request(
            "GET",
            f"{API_BETA}/{API_MARKETS}/{API_FUNDAMENTALS}/{API_CALENDARS}",
            params=params,
        )
        self._api_raw_data[RAW_CALENDARS] = res

        return res

    async def api_get_dividends(self, symbols: list[str]) -> dict[str, Any]:
        """Get dividend information for a security. This will include previous
        dividends as well as formally announced future dividend dates."""

        params = {"symbols": ",".join(symbols)}
        res = await self._api_request(
            "GET",
            f"{API_BETA}/{API_MARKETS}/{API_FUNDAMENTALS}/{API_DIVIDENDS}",
            params=params,
        )
        self._api_raw_data[RAW_DIVIDENDS] = res

        return res

    ############# Trading

    async def api_place_equity_order(
        self,
        account_id: str,
        order_class: OrderClass,
        symbol: str,
        side: EquityOrderSide,
        quantity: int,
        order_type: OrderType,
        duration: OrderDuration,
        price: float | None = None,
        stop: float | None = None,
        tag: str | None = None,
    ) -> dict[str, Any]:
        """Place an order to trade an equity security."""

        params = {
            "class": str(order_class),
            "symbol": symbol,
            "side": str(side),
            "quantity": str(quantity),
            "order_type": str(order_type),
            "duration": str(duration),
        }
        if price:
            params["price"] = str(price)
        if stop:
            params["stop"] = str(stop)
        if tag:
            # FIXME validate Maximum lenght of 255 characters. Valid characters are letters, numbers and -
            params["tag"] = tag

        res = await self._api_request(
            "POST",
            f"{API_V1}/{API_ACCOUNTS}/{account_id}/{API_ORDERS}",
            params=params,
        )
        self._api_raw_data[RAW_PLACE_EQUITY_ORDER] = res

        return res

    async def api_place_option_order(
        self,
        account_id: str,
        order_class: OrderClass,
        symbol: str,
        option_symbol: str,
        side: OptionOrderSide,
        quantity: int,
        order_type: OrderType,
        duration: OrderDuration,
        price: float | None = None,
        stop: float | None = None,
        tag: str | None = None,
    ) -> dict[str, Any]:
        """Place an order to trade a single option."""

        params = {
            "class": str(order_class),
            "symbol": symbol,
            "option_symbol": option_symbol,
            "side": str(side),
            "quantity": str(quantity),
            "order_type": str(order_type),
            "duration": str(duration),
        }
        if price:
            params["price"] = str(price)
        if stop:
            params["stop"] = str(stop)
        if tag:
            # FIXME validate Maximum lenght of 255 characters. Valid characters are letters, numbers and -
            params["tag"] = tag

        res = await self._api_request(
            "POST",
            f"{API_V1}/{API_ACCOUNTS}/{account_id}/{API_ORDERS}",
            params=params,
        )
        self._api_raw_data[RAW_PLACE_OPTION_ORDER] = res

        return res

    def raw_data(self) -> dict[str, Any]:
        """Return raw API data."""
        return self._api_raw_data
