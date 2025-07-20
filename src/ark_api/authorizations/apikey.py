from .arkauthorization import ArkAuthorization
from ark_api.utils import verify


class ApiKey(ArkAuthorization):
    def __init__(self, api_key):
        verify(api_key, "Secret", "api_key must be Secret")
        self._header = {"apikey": api_key.use()}
