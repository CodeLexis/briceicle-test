from .base import APIError, DEFAULT_ERROR_MESSAGE


_ERROR_CODE = 403


class ForbiddenError(APIError):
    code = _ERROR_CODE
    message = DEFAULT_ERROR_MESSAGE  # 'An internal server error occurred!'


class BadRequest(ForbiddenError):
    message = 'Bad request'


class ResourcesNotRelated(ForbiddenError):
    message = 'Resources not related'
