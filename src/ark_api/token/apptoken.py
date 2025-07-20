from .arktoken import ArkToken
from ark_api.utils import verify
from ark_api.discovery import Discovery
from ark_api.authorizations import Basic, AppBearer


class AppToken(ArkToken):
    _GEN_TOKEN = "token"
    _INTROSPECT_TOKEN = "introspect"
    _REVOKE_TOKEN = "revoke"
    _API_PATH_FORMAT = "{}/oauth2/{}/{}"

    def __init__(self, app_id, scope, subdomain, username, password):
        verify(app_id, "str", "app_id must be str")
        verify(scope, "str", "scope must be str")
        verify(subdomain, "str", "subdomain must be str")
        verify(username, "str", "username must be str")
        verify(password, "Secret", "password must be Secret")
        discovery = Discovery(subdomain)
        self._gen_api_path = self._API_PATH_FORMAT.format(
            discovery.endpoint,
            self._GEN_TOKEN,
            app_id
        )
        self._introspect_api_path = self._API_PATH_FORMAT.format(
            discovery.endpoint,
            self._INTROSPECT_TOKEN,
            app_id
        )
        self._revoke_api_path = self._API_PATH_FORMAT.format(
            discovery.endpoint,
            self._REVOKE_TOKEN,
            app_id
        )
        params = {"grant_type": "client_credentials", "scope": scope}
        auth = Basic(username, password)
        headers = {
            **auth.header,
            "Content-Type": "application/x-www-form-urlencoded"
        }
        method = "POST"
        self._subdomain = subdomain
        self._response = self.api_call(
            self._gen_api_path,
            method,
            headers,
            params
        )
        self._access_token = self._response.access_token
        self._jwt = self._get_unverified_claims(self._access_token)

    def introspect(self):
        auth = AppBearer(self)
        headers = {
            **auth.header,
            "Content-Type": "application/x-www-form-urlencoded"
        }
        method = "POST"
        params = {"token": self._access_token}
        response = self.api_call(
            self._introspect_api_path,
            method,
            headers,
            params
        )
        return response

    def revoke(self, username, password):
        verify(username, "str", "username must be str")
        verify(password, "Secret", "password must be Secret")
        auth = Basic(username, password)
        headers = {
            **auth.header,
            "Content-Type": "application/x-www-form-urlencoded"
        }
        method = "POST"
        params = {"token": self._access_token}
        response = self._api_call(
            self._revoke_api_path,
            method,
            headers,
            params
        )
        return response.code
