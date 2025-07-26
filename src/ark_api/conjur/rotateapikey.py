from ark_api.model import ArkApiCall
from ark_api.utils import api_call
from ark_api.utils import verify, Secret
from urllib.parse import urlencode


class RotateApiKey(ArkApiCall):
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
        response = api_call(api_path, method, headers)
        self._response = Secret(response.text())
