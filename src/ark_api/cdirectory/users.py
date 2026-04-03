from ark_api.model import ArkApiCall
from ark_api.utils import verify, api_call
from ark_api.discovery import Discovery


class GetUserByName(ArkApiCall):
    _API_PATH_FORMAT = "{}/CDirectoryService/GetUserByName"

    def __init__(self, auth, username):
        verify(auth, "PlatformBearer", "auth must be PlatformBearer")
        verify(username, "str", "username must be str")
        discovery = Discovery(auth.token.subdomain)
        api_path = self._API_PATH_FORMAT.format(discovery.response["endpoint"])
        params = {"username": username}
        headers = {
            **auth.header,
            "Content-Type": "application/json"
        }
        method = "POST"
        ark_api_response = api_call(api_path, method, headers, params)
        self._response = ark_api_response.json()
