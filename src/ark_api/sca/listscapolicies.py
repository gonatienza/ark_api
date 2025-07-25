from ark_api.api import Api
from ark_api.utils import verify


class ListScaPolicies(Api):
    _API_PATH_FORMAT = "https://{}.sca.cyberark.cloud/api/policies"

    def __init__(self, auth):
        verify(auth, "PlatformBearer", "auth must be PlatformBearer")
        api_path = self._API_PATH_FORMAT.format(auth.token.subdomain)
        params = {}
        headers = {
            **auth.header,
            "Content-Type": "application/json"
        }
        method = "GET"
        self._response = self.json_api_call(api_path, method, headers, params)

    @property
    def hits(self):
        return self._response.hits
