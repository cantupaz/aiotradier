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
    API_EXPIRATIONS,
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
    RAW_BALANCES,
    RAW_CHAINS,
    RAW_EXPIRATIONS,
    RAW_POSITIONS,
    RAW_STRIKES,
    RAW_USER_PROFILE,
    RAW_QUOTES,
)

_LOGGER = logging.getLogger(__name__)


class TradierRestAdapter:
    """Access Tradier API."""

    def __init__(
        self,
        aiohttp_session: ClientSession | None,
        token: str = "",
    ):
        """Set up the Adapter."""

        self.aiohttp_session: ClientSession | None = aiohttp_session
        self.token = token

        self._api_raw_data: dict[str, Any] = {
            RAW_USER_PROFILE: {},
            RAW_BALANCES: {},
            RAW_POSITIONS: {},
            RAW_QUOTES: {},
            RAW_CHAINS: {},
            RAW_EXPIRATIONS: {},
            RAW_STRIKES: {},
        }

    async def _api_request(
        self,
        method: str,
        path: str,
        payload: Any | None = None,
        params: Any | None = None,
    ) -> dict[str, Any]:
        """Tradier API request."""

        _LOGGER.debug("aiohttp request: /%s (params=%s)", path, payload)

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
        res = await self._api_request(
            "GET",
            f"{API_USER}/{API_PROFILE}",
        )
        self._api_raw_data[RAW_USER_PROFILE] = res

        return res

    async def api_get_balances(self, account_id) -> dict[str, Any]:
        res = await self._api_request(
            "GET", f"{API_ACCOUNTS}/{account_id}/{API_BALANCES}"
        )
        self._api_raw_data[RAW_BALANCES] = res

        return res

    async def api_get_positions(self, account_id) -> dict[str, Any]:
        res = await self._api_request(
            "GET", f"{API_ACCOUNTS}/{account_id}/{API_POSITIONS}"
        )
        self._api_raw_data[RAW_POSITIONS] = res

        return res

    async def api_get_quotes(
        self, symbols: list[str], greeks: bool = False
    ) -> dict[str, Any]:
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
