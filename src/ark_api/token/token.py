from ._arktoken import _ArkToken
from ark_api.discovery import Discovery


class Token(_ArkToken):
    _API_PATH_FORMAT = "{}/oauth2/platformtoken"

    def __init__(self, subdomain, username, password):
        assert isinstance(subdomain, str), "subdomain must be str"
        discovery = Discovery(subdomain)
        api_path = self._API_PATH_FORMAT.format(discovery.endpoint)
        super().__init__(api_path, username, password)
