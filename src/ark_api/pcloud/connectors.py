from ark_api.model import ArkApiCall
from ark_api.utils import api_call
from ark_api.utils import verify


class Connectors(ArkApiCall):
    _API_PATH_FORMAT = ("https://{}.connectormanagement.cyberark.cloud/api/connectors")
    def __init__(self, auth):
        verify(auth, "PlatformBearer", "auth must be PlatformBearer")
        api_path = self._API_PATH_FORMAT.format(auth.token.subdomain)
        headers = {
            **auth.header,
            "Content-Type": "application/json"
        }
        method = "GET"
        response = api_call(api_path, method, headers)
        self._response = response.json()
