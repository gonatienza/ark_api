from ark_api.api import Api
from ark_api.authorization import Bearer


class ListScaPolicies(Api):
    _API_PATH_FORMAT = "https://{}.sca.cyberark.cloud/api/policies"

    def __init__(self, auth):
        assert isinstance(auth, Bearer), "auth must be Bearer"
        api_path = self._API_PATH_FORMAT.format(auth.token.jwt.subdomain)
        params = {}
        headers = {
            **auth.header,
            "Content-Type": "application/json"
        }
        method = "GET"
        self._response = self.api_call(api_path, method, headers, params)

    @property
    def hits(self):
        return self._response.hits
