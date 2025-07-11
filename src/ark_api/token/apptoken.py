from .arktoken import ArkToken
from ark_api.utils import Secret
from ark_api.discovery import Discovery
from base64 import b64encode


class AppToken(ArkToken):
    _API_PATH_FORMAT = "{}/oauth2/token/{}"

    def __init__(self, app_id, scope, subdomain, username, password):
        assert isinstance(app_id, str), "app_id must be str"
        assert isinstance(scope, str), "scope must be str"
        assert isinstance(subdomain, str), "subdomain must be str"
        assert isinstance(username, str), "username must be str"
        assert isinstance(password, Secret), "password must be Secret"
        discovery = Discovery(subdomain)
        api_path = self._API_PATH_FORMAT.format(discovery.endpoint, app_id)
        params = {"grant_type": "client_credentials", "scope": scope}
        creds = f"{username}:{password.use()}"
        encoded_creds = b64encode(creds.encode())
        authorization = Secret(f"Basic {encoded_creds.decode()}")
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": authorization.use()
        }
        method = "POST"
        self._response = self.api_call(api_path, method, headers, params)
        self._access_token = self._response.access_token
        self._jwt = self._get_unverified_claims(self._access_token)
