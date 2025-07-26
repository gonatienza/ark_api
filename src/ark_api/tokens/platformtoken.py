from .jwttoken import JwtToken
from ark_api.utils import verify, Secret, api_call
from ark_api.discovery import Discovery


class PlatformToken(JwtToken):
    _API_PATH_FORMAT = "{}/oauth2/platformtoken"

    def __init__(self, subdomain, username, password):
        verify(subdomain, "str", "subdomain must be str")
        verify(username, "str", "username must be str")
        verify(password, "Secret", "password must be Secret")
        self._subdomain = subdomain
        discovery = Discovery(self._subdomain)
        api_path = self._API_PATH_FORMAT.format(discovery.response["endpoint"])
        params = {
            "grant_type": "client_credentials",
            "client_id": username,
            "client_secret": password.get()
        }
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        method = "POST"
        response = api_call(api_path, method, headers, params)
        self._response = response.json()
        self._access_token = Secret(self._response["access_token"])
        self._jwt = self._get_unverified_claims(self._access_token.get())
