from ark_api.api import Api
from ark_api.utils import verify


class Safes(Api):
    _API_PATH_FORMAT = (
        "https://{}.privilegecloud.cyberark.cloud/PasswordVault/API/Safes/"
    )

    def __init__(self, auth):
        verify(auth, "PlatformBearer", "auth must be PlatformBearer")
        api_path = self._API_PATH_FORMAT.format(auth.token.jwt.subdomain)
        params = {
            "includeAccounts": True,
            "extendedDetails": True
        }
        headers = {
            **auth.header,
            "Content-Type": "application/json"
        }
        method = "GET"
        self._response = self.api_call(api_path, method, headers, params)

    @property
    def value(self):
        return self._response.value
