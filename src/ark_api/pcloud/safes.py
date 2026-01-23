from ark_api.model import ArkApiCall
from ark_api.utils import api_call
from ark_api.utils import verify
from urllib.parse import urljoin


class Safes(ArkApiCall):
    _PCLOUD_PATH_FORMAT = (
        "https://{}.privilegecloud.cyberark.cloud/PasswordVault/"
    )
    _API_PATH_FORMAT = urljoin(_PCLOUD_PATH_FORMAT, "API/Safes/")

    def __init__(self, auth):
        verify(auth, "PlatformBearer", "auth must be PlatformBearer")
        self._subdomain = auth.token.subdomain
        api_path = self._API_PATH_FORMAT.format(self._subdomain)
        self._params = {
            "includeAccounts": True,
            "extendedDetails": True
        }
        self._headers = {
            **auth.header,
            "Content-Type": "application/json"
        }
        self._method = "GET"
        ark_api_response = api_call(
            api_path,
            self._method,
            self._headers,
            self._params
        )
        self._response = ark_api_response.json()

    def is_next_link(self):
        if "nextLink" in self._response:
            return True
        else:
            return False

    def get_next_link(self):
        if self.is_next_link():
            next_link = self._response["nextLink"]
            _api_path = self._PCLOUD_PATH_FORMAT.format(self._subdomain)
            api_path = urljoin(_api_path, next_link)
            ark_api_response = api_call(
                api_path,
                self._method,
                self._headers,
                self._params
            )
            self._response = ark_api_response.json()
