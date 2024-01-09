"""Tradier API exceptions."""


class TradierError(Exception):
    """Base class for Tradier exceptions."""


class APIError(TradierError):
    """Exception raised when API fails."""


class LoginError(TradierError):
    """Exception raised when login fails."""


class AuthError(LoginError):
    """Exception raised when API denies access."""
