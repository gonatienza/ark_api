from ark_api.model import ArkApiCall
from ark_api.utils import api_call
from ark_api.utils import verify


class Discovery(ArkApiCall):
    _API_PATH_FORMAT = (
        "https://platform-discovery.cyberark.cloud/"
        "api/identity-endpoint/{}"
    )

    def __init__(self, subdomain):
        verify(subdomain, "str", "subdomain must be str")
        api_path = self._API_PATH_FORMAT.format(subdomain)
        headers = {"Content-Type": "application/json"}
        method = "GET"
        response = api_call(api_path, method, headers)
        self._response = response.json()
