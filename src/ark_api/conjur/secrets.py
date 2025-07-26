from ark_api.api import Api
from ark_api.utils import verify, Secret
from urllib.parse import quote, urlencode


class ListSecrets(Api):
    _API_PATH_FORMAT = "https://{}.secretsmgr.cyberark.cloud/api/resources"

    def __init__(self, auth):
        verify(auth, "ConjurBearer", "auth must be ConjurBearer")
        api_path = self._API_PATH_FORMAT.format(auth.token.subdomain)
        headers = auth.header
        method = "GET"
        self._response = self.json_api_call(api_path, method, headers)


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
        response = self.api_call(api_path, method, headers)
        response_bytes = response.read()
        self._response = Secret(response_bytes.decode())


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
        response = self.json_api_call(api_path, method, headers)
        self._response = {
            item: Secret(response[item])
            for item in response
        }
