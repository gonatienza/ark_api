from ark_api.api import Api
from ark_api.utils import verify


class SafeMembers(Api):
    _API_PATH_FORMAT = (
        "https://{}.privilegecloud.cyberark.cloud/"
        "PasswordVault/API/Safes/{}/Members/"
    )

    def __init__(self, auth, safe_url_id):
        verify(auth, "PlatformBearer", "auth must be PlatformBearer")
        verify(safe_url_id, "str", "safe_name must be str")
        api_path = self._API_PATH_FORMAT.format(
            auth.token.subdomain,
            safe_url_id
        )
        params = {"safeUrlId": safe_url_id}
        headers = {
            **auth.header,
            "Content-Type": "application/json"
        }
        method = "GET"
        self._response = self.json_api_call(api_path, method, headers, params)

    @property
    def value(self):
        return self._response.value
