from .arkauthorization import ArkAuthorization
from abc import abstractmethod
from ark_api.utils import verify


class ApiKey(ArkAuthorization):
    @abstractmethod
    def __init__(self):
        pass

    @property
    def api_key(self):
        return self._api_key


class FlowsApiKey(ApiKey):
    def __init__(self, api_key):
        verify(api_key, "Secret", "api_key must be Secret")
        self._api_key = api_key.get()
        self._header = {"apikey": self._api_key}


class ConjurApiKey(ApiKey):
    def __init__(self, api_key):
        verify(api_key, "Secret", "api_key must be Secret")
        self._api_key = api_key.get()
        self._header = {}
