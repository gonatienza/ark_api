from ark_api.model import ArkApiCall
from ark_api.utils import api_call
from ark_api.utils import verify


class SafeMembers(ArkApiCall):
    _API_PATH_FORMAT = (
        "https://{}.privilegecloud.cyberark.cloud/"
        "PasswordVault/API/Safes/{}/Members/"
    )

    def __init__(self, auth, safe_url_id, params):
        verify(auth, "PlatformBearer", "auth must be PlatformBearer")
        verify(safe_url_id, "str", "safe_name must be str")
        verify(params, "dict", "params must be dict")
        api_path = self._API_PATH_FORMAT.format(
            auth.token.subdomain,
            safe_url_id
        )
        headers = {
            **auth.header,
            "Content-Type": "application/json"
        }
        method = "POST"
        response = api_call(api_path, method, headers, params)
        self._response = response.json()
