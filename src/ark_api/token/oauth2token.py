from ._arktoken import _ArkToken
from ark_api.discovery import Discovery


class Oauth2Token(_ArkToken):
    _API_PATH_FORMAT = "{}/oauth2/token/{}"

    def __init__(self, app_id, subdomain, username, password):
        assert isinstance(app_id, str), "app_id must be str"
        assert isinstance(subdomain, str), "subdomain must be str"
        discovery = Discovery(subdomain)
        api_path = self._API_PATH_FORMAT.format(discovery.endpoint, app_id)
        super().__init__(api_path, username, password)
