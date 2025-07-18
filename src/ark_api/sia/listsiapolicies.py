from ark_api.api import Api
from ark_api.utils import verify


class ListSiaPolicies(Api):
    _API_PATH_FORMAT = "https://{}.dpa.cyberark.cloud/api/access-policies"

    def __init__(self, auth):
        verify(auth, "PlatformBearer", "auth must be PlatformBearer")
        api_path = self._API_PATH_FORMAT.format(auth.token.jwt.subdomain)
        params = {}
        headers = {
            **auth.header,
            "Content-Type": "application/json"
        }
        method = "GET"
        self._response = self.api_call(api_path, method, headers, params)

    @property
    def items(self):
        return self._response.items
