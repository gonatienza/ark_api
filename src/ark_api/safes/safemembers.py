from ark_api.model import ArkApiCall
from ark_api.utils import api_call
from ark_api.utils import verify


_API_PATH_FORMAT = (
        "https://{}.privilegecloud.cyberark.cloud/"
        "PasswordVault/API/Safes/{}/Members/"
    )


class SafeMembers(ArkApiCall):
    def __init__(self, auth, safe_url_id):
        verify(auth, "PlatformBearer", "auth must be PlatformBearer")
        verify(safe_url_id, "str", "safe_name must be str")
        api_path = _API_PATH_FORMAT.format(
            auth.token.subdomain,
            safe_url_id
        )
        headers = {
            **auth.header,
            "Content-Type": "application/json"
        }
        method = "GET"
        response = api_call(api_path, method, headers)
        self._response = response.json()


class AddSafeMembers(ArkApiCall):
    def __init__(self, auth, safe_url_id, params):
        verify(auth, "PlatformBearer", "auth must be PlatformBearer")
        verify(safe_url_id, "str", "safe_name must be str")
        verify(params, "dict", "params must be dict")
        api_path = _API_PATH_FORMAT.format(
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
