from .arkauthorization import ArkAuthorization
from ark_api.utils import Secret, verify


class Bearer(ArkAuthorization):
    def __init__(self, token):
        verify(token, "ArkToken", "token must be ArkToken")
        self._token = token

    @property
    def token(self):
        return self._token


class JwtBearer(Bearer):
    def __init__(self, token):
        verify(token, "JwtToken", "token must be JwtToken")
        super().__init__(token)
        authorization = Secret(f"Bearer {self._token.access_token.get()}")
        self._header = {"Authorization": authorization.get()}


class PlatformBearer(JwtBearer):
    def __init__(self, token):
        verify(token, "PlatformToken", "token must be PlatformToken")
        super().__init__(token)


class AppBearer(JwtBearer):
    def __init__(self, token):
        verify(token, "AppToken", "token must be AppToken")
        super().__init__(token)


class ConjurBearer(Bearer):
    def __init__(self, token):
        verify(token, "ConjurToken", "token must be ConjurToken")
        super().__init__(token)
        authorization = Secret(
            f'Token token="{self._token.access_token.get()}"'
        )
        self._header = {"Authorization": authorization.get()}
