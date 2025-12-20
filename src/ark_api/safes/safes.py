from ark_api.model import ArkApiCall
from ark_api.utils import api_call
from ark_api.utils import verify


class Safes(ArkApiCall):
    __API_PATH_FORMAT = (
        "https://{}.privilegecloud.cyberark.cloud/PasswordVault/"
    )
    _API_PATH_FORMAT = __API_PATH_FORMAT + "API/Safes/"

    def __init__(self, auth, next_link=None):
        verify(auth, "PlatformBearer", "auth must be PlatformBearer")
        if next_link:
            verify(next_link, "str", "next_link must be str")
            _api_path = self.__API_PATH_FORMAT.format(auth.token.subdomain)
            api_path = _api_path + next_link
        else:
            api_path = self._API_PATH_FORMAT.format(auth.token.subdomain)
        params = {
            "includeAccounts": True,
            "extendedDetails": True
        }
        headers = {
            **auth.header,
            "Content-Type": "application/json"
        }
        method = "GET"
        response = api_call(api_path, method, headers, params)
        self._response = response.json()
