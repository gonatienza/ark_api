from ark_api.api import Api
from ark_api.utils import verify


class Discovery(Api):
    _API_PATH_FORMAT = (
        "https://platform-discovery.cyberark.cloud/"
        "api/identity-endpoint/{}"
    )

    def __init__(self, subdomain):
        verify(subdomain, "str", "subdomain must be str")
        api_path = self._API_PATH_FORMAT.format(subdomain)
        headers = {"Content-Type": "application/json"}
        params = None
        method = "GET"
        self._response = self.api_call(api_path, method, headers, params)

    @property
    def endpoint(self):
        return self._response.endpoint
