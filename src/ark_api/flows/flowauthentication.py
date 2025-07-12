from ark_api.utils import Secret
from base64 import b64encode
from abc import ABC, abstractmethod


class FlowAuthentication(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @property
    def headers(self):
        return self._headers


class Basic(FlowAuthentication):
    def __init__(self, username, password):
        assert isinstance(username, str), "username must be str"
        assert isinstance(password, Secret), "password must be Secret"
        creds = f"{username}:{password.use()}"
        encoded_creds = b64encode(creds.encode())
        authorization = Secret(f"Basic {encoded_creds.decode()}")
        self._headers = {"Authorization": authorization.use()}


class Bearer(FlowAuthentication):
    def __init__(self, token):
        assert isinstance(token, Secret), "token must be Secret"
        authorization = Secret(f"Bearer {token.use()}")
        self._headers = {"Authorization": authorization.use()}


class ApiKey(FlowAuthentication):
    def __init__(self, api_key):
        assert isinstance(api_key, Secret), "pasapi_keysword must be Secret"
        self._headers = {"apikey": api_key.use()}
