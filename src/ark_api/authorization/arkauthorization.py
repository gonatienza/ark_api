from ark_api.token import PlatformToken
from ark_api.utils import Secret
from base64 import b64encode
from abc import ABC, abstractmethod


class ArkAuthorization(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @property
    def header(self):
        return self._header


class Basic(ArkAuthorization):
    def __init__(self, username, password):
        assert isinstance(username, str), "username must be str"
        assert isinstance(password, Secret), "password must be Secret"
        creds = f"{username}:{password.use()}"
        encoded_creds = b64encode(creds.encode())
        authorization = Secret(f"Basic {encoded_creds.decode()}")
        self._header = {"Authorization": authorization.use()}


class Bearer(ArkAuthorization):
    def __init__(self, token):
        assert isinstance(token, PlatformToken), "token must be PlatformToken"
        self._token = token
        authorization = Secret(f"Bearer {self._token.access_token}")
        self._header = {"Authorization": authorization.use()}

    @property
    def token(self):
        return self._token


class ApiKey(ArkAuthorization):
    def __init__(self, api_key):
        assert isinstance(api_key, Secret), "api_key must be Secret"
        self._header = {"apikey": api_key.use()}
