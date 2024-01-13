"""Tradier API exceptions."""


class TradierError(Exception):
    """Base class for Tradier exceptions."""


class APIError(TradierError):
    """Exception raised when API fails."""


class AuthError(LoginError):
    """Exception raised when API denies access."""
