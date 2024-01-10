"""Provide AsyncIO access to Tradier API"""

import asyncio
import logging
from datetime import date
import json
from typing import Any, cast
from aiohttp import ClientConnectorError, ClientResponseError, ClientSession

from .exceptions import TradierError, LoginError, APIError, AuthError
from .const import (
    API_ACCOUNTS,
    API_BALANCES,
    API_CHAINS,
    API_CLOCK,
    API_EXPIRATIONS,
    API_HISTORY,
    API_MARKETS,
    API_OPTIONS,
    API_POSITIONS,
    API_PROFILE,
    API_QUOTES,
    API_STRIKES,
    API_URL,
    API_USER,
    API_V1,
    HTTP_CALL_TIMEOUT,
    RAW_ACCOUNT_HISTORY,
    RAW_BALANCES,
    RAW_CHAINS,
    RAW_CLOCK,
    RAW_EXPIRATIONS,
    RAW_HISTORICAL_QUOTES,
    RAW_POSITIONS,
    RAW_STRIKES,
    RAW_USER_PROFILE,
    RAW_QUOTES,
)

_LOGGER = logging.getLogger(__name__)


class TradierAPIAdapter:
    """Access Tradier API."""

    def __init__(
        self,
        aiohttp_session: ClientSession | None,
        token: str = "",
    ):
        """Set up the Adapter."""

        self.aiohttp_session: ClientSession | None = aiohttp_session
        self.token = token

        self._api_raw_data: dict[str, Any] = {}

    async def _api_request(
        self,
        method: str,
        path: str,
        payload: Any | None = None,
        params: Any | None = None,
    ) -> dict[str, Any]:
        """Tradier API request."""

        _LOGGER.debug(
            "aiohttp request: /%s (params=%s) (payload=%s)", path, params, payload
        )

        if self.aiohttp_session is None:
            aiohttp_session = ClientSession()
        else:
            aiohttp_session = self.aiohttp_session

        headers = {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/json",
        }

        try:
            async with aiohttp_session.request(
                method,
                f"{API_URL}/{API_V1}/{path}",
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
            # if err.status == 429:
            #     raise TooManyRequests(err) from err
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

    async def api_get_user_profile(self) -> dict[str, Any]:
        "Get user profile (includes account metadata)."
        res = await self._api_request(
            "GET",
            f"{API_USER}/{API_PROFILE}",
        )
        self._api_raw_data[RAW_USER_PROFILE] = res

        return res

    async def api_get_balances(self, account_id) -> dict[str, Any]:
        """Get account balances."""
        res = await self._api_request(
            "GET", f"{API_ACCOUNTS}/{account_id}/{API_BALANCES}"
        )
        self._api_raw_data[RAW_BALANCES] = res

        return res

    async def api_get_positions(self, account_id) -> dict[str, Any]:
        """Get account positions."""
        res = await self._api_request(
            "GET", f"{API_ACCOUNTS}/{account_id}/{API_POSITIONS}"
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
            params["end"] = (end.strftime("%Y-%m-%d"),)
        if symbol:
            params["symbol"] = symbol
        if exact_match:
            params["exact_match"] = f"{exact_match}"

        res = await self._api_request(
            "GET", f"{API_ACCOUNTS}/{account_id}/{API_HISTORY}", params=params
        )
        self._api_raw_data[RAW_ACCOUNT_HISTORY] = res

        return res

    async def api_get_quotes(
        self, symbols: list[str], greeks: bool = False
    ) -> dict[str, Any]:
        """Get quote info."""
        params = {"symbols": ",".join(symbols), "greeks": f"{greeks}"}
        res = await self._api_request(
            "GET", f"{API_MARKETS}/{API_QUOTES}", params=params
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
        """Get a list of option expirations."""
        params = {
            "symbol": symbol,
            "includeAllRoots": f"{include_all_roots}",
            "strikes": f"{strikes}",
            "contractSize": f"{contract_size}",
            "expirationType": f"{expiration_type}",
        }

        res = await self._api_request(
            "GET", f"{API_MARKETS}/{API_OPTIONS}/{API_EXPIRATIONS}", params=params
        )
        self._api_raw_data[RAW_EXPIRATIONS] = res

        return res

    async def api_get_option_strikes(
        self,
        symbol: str,
        expiration: date,
    ) -> dict[str, Any]:
        """Get a list of option strikes."""
        params = {
            "symbol": symbol,
            "expiration": expiration.strftime("%Y-%m-%d"),
        }

        res = await self._api_request(
            "GET", f"{API_MARKETS}/{API_OPTIONS}/{API_STRIKES}", params=params
        )
        self._api_raw_data[RAW_STRIKES] = res

        return res

    async def api_get_option_chains(
        self, symbol: str, expiration: date, greeks: bool = False
    ) -> dict[str, Any]:
        """Get options chains."""
        params = {
            "symbol": symbol,
            "expiration": expiration.strftime("%Y-%m-%d"),
            "greeks": f"{greeks}",
        }

        res = await self._api_request(
            "GET", f"{API_MARKETS}/{API_OPTIONS}/{API_CHAINS}", params=params
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
            "GET", f"{API_MARKETS}/{API_HISTORY}", params=params
        )
        self._api_raw_data[RAW_HISTORICAL_QUOTES] = res

        return res

    async def api_get_clock(self, delayed: bool = False) -> dict[str, Any]:
        """Get the intraday market status.
        This call will change and return information pertaining to the current
        day. If programming logic on whether the market is open/closed – this
        API call should be used to determine the current state."""

        params = {"delayed": f"{delayed}"}

        res = await self._api_request(
            "GET", f"{API_MARKETS}/{API_CLOCK}", params=params
        )
        self._api_raw_data[RAW_CLOCK] = res

        return res

    # async def api_get_installations(self) -> dict[str, Any]:
    #     """Request API installations data."""
    #     res = await self.api_request(
    #         "GET",
    #         f"{API_V1}/{API_INSTALLATIONS}",
    #     )
    #     self._api_raw_data[RAW_INSTALLATIONS_LIST] = res

    #     return res

    # async def list_installations(self) -> list[Installation]:
    #     """Return Airzone Cloud installations list."""
    #     inst_list: list[Installation] = []

    #     inst_data = await self.api_get_installations()
    #     for inst in inst_data[API_INSTALLATIONS]:
    #         inst_list += [Installation(inst)]

    #     return inst_list

    def raw_data(self) -> dict[str, Any]:
        """Return raw Airzone Cloud API data."""
        return self._api_raw_data
