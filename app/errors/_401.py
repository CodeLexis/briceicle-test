from .base import APIError, DEFAULT_ERROR_MESSAGE


_ERROR_CODE = 401


class AuthenticationError(APIError):
    code = _ERROR_CODE
    message = DEFAULT_ERROR_MESSAGE  # 'An internal server error occurred!'


class InvalidToken(AuthenticationError):
    message = 'Invalid authentication token provided.'


class TokenExpired(AuthenticationError):
    message = 'Token has expired.'


class UnsuccessfulAuthentication(AuthenticationError):
    message = 'Authentication unsuccessful'
