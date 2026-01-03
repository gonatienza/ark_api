from .arkauthorization import ArkAuthorization
from ark_api.utils import Secret, verify
from abc import abstractmethod


class Bearer(ArkAuthorization):
    @abstractmethod
    def __init__(self):
        """
        Following attributes required:
        _header
        _token
        """

    @property
    def token(self):
        return self._token


class JwtBearer(Bearer):
    def __init__(self, token):
        verify(token, "JwtToken", "token must be JwtToken")
        self._token = token
        authorization = Secret(f"Bearer {self._token.access_token.get()}")
        self._header = {"Authorization": authorization.get()}


class PlatformBearer(JwtBearer):
    def __init__(self, token):
        verify(token, "PlatformToken", "token must be PlatformToken")
        super().__init__(token)
        self._token = token


class AppBearer(JwtBearer):
    def __init__(self, token):
        verify(token, "AppToken", "token must be AppToken")
        super().__init__(token)
        self._token = token


class ConjurBearer(Bearer):
    def __init__(self, token):
        verify(token, "ConjurToken", "token must be ConjurToken")
        self._token = token
        authorization = Secret(
            f'Token token="{self._token.access_token.get()}"'
        )
        self._header = {"Authorization": authorization.get()}


class EpmBearer(Bearer):
    def __init__(self, token):
        verify(token, "EpmToken", "token must be EpmToken")
        self._token = token
        authorization = Secret(
            f"basic {self._token.access_token.get()}"
        )
        self._header = {"Authorization": authorization.get()}
