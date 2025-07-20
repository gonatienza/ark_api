from .arkauthorization import ArkAuthorization
from ark_api.utils import Secret, verify


class Bearer(ArkAuthorization):
    def __init__(self, token):
        verify(token, "ArkToken", "token must be ArkToken")
        self._token = token
        authorization = Secret(f"Bearer {self._token.access_token}")
        self._header = {"Authorization": authorization.use()}

    @property
    def token(self):
        return self._token


class PlatformBearer(Bearer):
    def __init__(self, token):
        verify(token, "PlatformToken", "token must be PlatformToken")
        super().__init__(token)


class AppBearer(Bearer):
    def __init__(self, token):
        verify(token, "AppToken", "token must be AppToken")
        super().__init__(token)
