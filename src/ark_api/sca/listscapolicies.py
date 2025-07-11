from ark_api.api import Api
from ark_api.utils import Secret


class ListScaPolicies(Api):
    _API_PATH_FORMAT = "https://{}.sca.cyberark.cloud/api/policies"

    def __init__(self, token, subdomain):
        assert isinstance(token, str), "token must be str"
        assert isinstance(subdomain, str), "subdomain must be str"
        api_path = self._API_PATH_FORMAT.format(subdomain)
        params = {}
        authorization = Secret(f"Bearer {token}")
        headers = {
            "Content-Type": "application/json",
            "Authorization": authorization.use()
        }
        method = "GET"
        self._response = self.api_call(headers, params, api_path, method)

    @property
    def hits(self):
        return self._response.hits
