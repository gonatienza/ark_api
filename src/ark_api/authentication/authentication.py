from ark_api.utils import verify, Secret, api_call
from ark_api.model import ArkApiCall
from ark_api.discovery import Discovery
from ark_api.exceptions import APIError
from ark_api.tokens import PlatformToken


class Authentication(ArkApiCall):
    _API_PATH_FORMAT_START = "{}/Security/StartAuthentication"
    _API_PATH_FORMAT_ADVANCE = "{}/Security/AdvanceAuthentication"

    def __init__(self, subdomain, username):
        verify(subdomain, "str", "subdomain must be str")
        verify(username, "str", "username must be str")
        self._subdomain = subdomain
        discovery = Discovery(self._subdomain)
        self._start_api_path = self._API_PATH_FORMAT_START.format(
            discovery.response["endpoint"]
        )
        self._advance_api_path = self._API_PATH_FORMAT_ADVANCE.format(
            discovery.response["endpoint"]
        )
        params = {
            "Version": "1.0",
            "User": username
        }
        self._headers = {"Content-Type": "application/json"}
        self._method = "POST"
        response = api_call(
            self._start_api_path, self._method, self._headers, params
        )
        self._response = response.json()
        if not self._response["success"]:
            raise APIError(self._response["Message"])
        self._responses = [self._response]
        self._session_id = self._response["Result"]["SessionId"]
        self._challenges = self._response["Result"]["Challenges"]
        self._token = None
        self._terminated = False

    @property
    def responses(self):
        return self._responses

    @property
    def session_id(self):
        return self._session_id

    @property
    def challenges(self):
        return self._challenges

    @property
    def token(self):
        return self._token

    @property
    def terminated(self):
        return self._terminated

    def get_mechanisms(self, index):
        verify(index, "int", "index must be int")
        return self._challenges[index]["Mechanisms"]

    def advance(self, params):
        if self._terminated:
            raise APIError("authentication has terminated")
        verify(params, "dict", "params must be dict")
        _response = api_call(
            self._advance_api_path, self._method, self._headers, params
        )
        response = _response.json()
        if not response["success"]:
            raise APIError(response["Message"])
        self._response = response
        self._responses.insert(0, self._response)
        if "Token" in self._response["Result"]:
            self._token = PlatformToken.from_string(
                self._subdomain, self._response["Result"]["Token"]
            )
            self._terminated = True
