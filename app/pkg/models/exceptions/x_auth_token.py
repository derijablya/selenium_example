from starlette import status

from app.pkg.models.base import BaseException

all = ["InvalidCredentials"]


class InvalidCredentials(BaseException):
    message = "Could not validate credentials."
    status_code = status.HTTP_403_FORBIDDEN
