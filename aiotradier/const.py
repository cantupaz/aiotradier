"""Tradier API constants."""

from typing import Final

API_URL: Final[str] = "https://sandbox.tradier.com"
API_V1: Final[str] = "v1"
API_USER = "user"
API_PROFILE = "profile"
API_ACCOUNTS: Final[str] = "accounts"
API_BALANCES: Final[str] = "balances"
API_POSITIONS: Final[str] = "positions"
API_MARKETS: Final[str] = "markets"
API_QUOTES: Final[str] = "quotes"
API_OPTIONS: Final[str] = "options"
API_EXPIRATIONS: Final[str] = "expirations"
API_STRIKES: Final[str] = "strikes"
API_CHAINS: Final[str] = "chains"
API_HISTORY: Final[str] = "history"
API_CLOCK: Final[str] = "clock"


HTTP_CALL_TIMEOUT: Final[int] = 45
HTTP_MAX_REQUESTS: Final[int] = 4

RAW_USER_PROFILE: Final[str] = "user_profile"
RAW_BALANCES: Final[str] = "balances"
RAW_POSITIONS: Final[str] = "positions"
RAW_QUOTES: Final[str] = "quotes"
RAW_EXPIRATIONS: Final[str] = "expirations"
RAW_CHAINS: Final[str] = "chains"
RAW_STRIKES: Final[str] = "strikes"
RAW_ACCOUNT_HISTORY: Final[str] = "account_history"
RAW_HISTORICAL_QUOTES: Final[str] = "historical_quotes"
RAW_CLOCK: Final[str] = "clock"
