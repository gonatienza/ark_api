from ark_api.api import Api
from ark_api.utils import verify
from urllib.parse import urlencode


class RotateApiKey(Api):
    _API_PATH_FORMAT = (
        "https://{}.secretsmgr.cyberark.cloud/api/"
        "authn/conjur/api_key"
    )

    def __init__(self, auth, identifier):
        verify(auth, "ConjurBearer", "auth must be ConjurBearer")
        verify(identifier, "str", "identifier must be str")
        _api_path = self._API_PATH_FORMAT.format(auth.token.subdomain)
        _params = urlencode({"role": f"host:{identifier}"})
        api_path = f"{_api_path}?{_params}"
        headers = auth.header
        method = "PUT"
        self._response = self.api_call(api_path, method, headers)
        api_key_bytes = self._response.read()
        self._api_key = api_key_bytes.decode()

    @property
    def api_key(self):
        return self._api_key
