"""Tradier API constants."""

from typing import Final

API_URL: Final[str] = "https://api.tradier.com"
API_SANDBOX_URL: Final[str] = "https://sandbox.tradier.com"
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
API_FUNDAMENTALS: Final[str] = "fundamentals"
API_CALENDARS: Final[str] = "calendars"
API_BETA: Final[str] = "beta"
API_DIVIDENDS: Final[str] = "dividends"
API_TIMESALES: Final[str] = "timesales"
API_SEARCH: Final[str] = "search"
API_LOOKUP: Final[str] = "lookup"
API_ORDERS: Final[str] = "orders"
API_COMPANY: Final[str] = "company"
API_CALENDAR: Final[str] = "calendar"
API_GAINLOSS: Final[str] = "gainloss"

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
RAW_CALENDARS: Final[str] = "corporate_calendars"
RAW_DIVIDENDS: Final[str] = "dividends"
RAW_TIMESALES: Final[str] = "timesales"
RAW_SEARCH: Final[str] = "search"
RAW_LOOKUP: Final[str] = "lookup"
RAW_PLACE_EQUITY_ORDER: Final[str] = "place_equity_order"
RAW_PLACE_OPTION_ORDER: Final[str] = "place_option_order"
RAW_COMPANY: Final[str] = "company"
RAW_CALENDAR: Final[str] = "market_calendar"
RAW_GAINLOSS: Final[str] = "gainloss"
RAW_ORDERS: Final[str] = "orders"
RAW_ORDER_DETAIL: Final[str] = "order_detail"
