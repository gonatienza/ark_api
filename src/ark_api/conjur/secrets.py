from ark_api.api import Api
from ark_api.utils import verify, Secret, ArkObject
from urllib.parse import quote, urlencode
import json


class ListSecrets(Api):
    _API_PATH_FORMAT = "https://{}.secretsmgr.cyberark.cloud/api/resources"

    def __init__(self, auth):
        verify(auth, "ConjurBearer", "auth must be ConjurBearer")
        api_path = self._API_PATH_FORMAT.format(auth.token.subdomain)
        headers = auth.header
        method = "GET"
        self._response = self.json_api_call(api_path, method, headers)
        self._secrets = self._response.items

    @property
    def secrets(self):
        return self._secrets


class GetSecret(Api):
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
        self._response = self.api_call(api_path, method, headers)
        response_bytes = self._response.read()
        self._secret = Secret(response_bytes.decode())

    @property
    def secret(self):
        return self._secret


class GetSecrets(Api):
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
        self._response = self.api_call(api_path, method, headers)
        response_bytes = self._response.read()
        response_str = response_bytes.decode()
        response_dict = json.loads(response_str)
        _response_dict = {
            item: Secret(response_dict[item])
            for item in response_dict
        }
        self._secrets = ArkObject(_response_dict)

    @property
    def secrets(self):
        return self._secrets
