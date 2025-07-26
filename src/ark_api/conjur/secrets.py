from ark_api.model import ArkApiCall
from ark_api.utils import api_call
from ark_api.utils import verify, Secret
from urllib.parse import quote, urlencode


class ListSecrets(ArkApiCall):
    _API_PATH_FORMAT = "https://{}.secretsmgr.cyberark.cloud/api/resources"

    def __init__(self, auth):
        verify(auth, "ConjurBearer", "auth must be ConjurBearer")
        api_path = self._API_PATH_FORMAT.format(auth.token.subdomain)
        headers = auth.header
        method = "GET"
        response = api_call(api_path, method, headers)
        self._response = response.json()


class GetSecret(ArkApiCall):
    _API_PATH_FORMAT = (
        "https://{}.secretsmgr.cyberark.cloud/api/"
        "secrets/conjur/variable"
    )

    def __init__(self, auth, secret):
        verify(auth, "ConjurBearer", "auth must be ConjurBearer")
        verify(secret, "str", "secret must be str")
        _api_path = self._API_PATH_FORMAT.format(auth.token.subdomain)
        _params = quote(secret)
        api_path = f"{_api_path}/{_params}"
        headers = auth.header
        method = "GET"
        response = api_call(api_path, method, headers)
        self._response = Secret(response.text())


class GetSecrets(ArkApiCall):
    _API_PATH_FORMAT = "https://{}.secretsmgr.cyberark.cloud/api/secrets"

    def __init__(self, auth, secrets):
        verify(auth, "ConjurBearer", "auth must be ConjurBearer")
        verify(secrets, "list", "secrets must be list")
        for secret in secrets:
            verify(secret, "str", "secret must be str")
        _api_path = self._API_PATH_FORMAT.format(auth.token.subdomain)
        variable_ids_list = [
            f"conjur:variable:{secret}"
            for secret in secrets
        ]
        variable_ids = ",".join(variable_ids_list)
        _params = urlencode({"variable_ids": variable_ids})
        api_path = f"{_api_path}?{_params}"
        headers = auth.header
        method = "GET"
        response = api_call(api_path, method, headers)
        json_response = response.json()
        self._response = {
            item: Secret(json_response[item])
            for item in json_response
        }
