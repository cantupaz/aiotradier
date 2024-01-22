"""Tradier API common code."""

from enum import auto, StrEnum


class SortBy(StrEnum):
    """Field to sort by in gainloss"""

    OPENDATE = auto()
    CLOSEDATE = auto()


class SortOrder(StrEnum):
    """Sort direction in gainloss"""

    ASC = auto()
    DESC = auto()


class OrderClass(StrEnum):
    """Represents the possible classes of orders (equity, option, etc.)"""

    EQUITY = auto()
    OPTION = auto()


class EquityOrderSide(StrEnum):
    """The side of the order (buy, sell, etc.)"""

    BUY = auto()
    BUY_TO_COVER = auto()
    SELL = auto()
    SELL_SHORT = auto()


class OptionOrderSide(StrEnum):
    """The side of the order (buy_to_open, sell_to_close, etc.)"""

    BUY_TO_OPEN = auto()
    BUY_TO_CLOSE = auto()
    SELL_TO_OPEN = auto()
    SELL_TO_CLOSE = auto()


class OrderType(StrEnum):
    """Represents the possible types of orders (market, limit, etc.)"""

    MARKET = auto()
    LIMIT = auto()
    STOP = auto()
    STOP_LIMIT = auto()


class MultiLegOrderType(StrEnum):
    """Represents the types of multi-leg option orders (market, debit, etc.)"""

    MARKET = auto()
    DEBIT = auto()
    CREDIT = auto()
    EVEN = auto()


class OrderDuration(StrEnum):
    """Time the order will remain active (day, gtc, etc.)"""

    DAY = auto()
    GTC = auto()
    PRE = auto()
    POST = auto()
