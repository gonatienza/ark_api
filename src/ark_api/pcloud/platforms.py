from ark_api.model import ArkApiCall
from ark_api.utils import api_call
from ark_api.utils import verify


class Platforms(ArkApiCall):
    _API_PATH_FORMAT = (
        "https://{}.privilegecloud.cyberark.cloud/PasswordVault/API/Platforms/"
    )

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


class GetPlatform(ArkApiCall):
    _API_PATH_FORMAT = (
        "https://{}.privilegecloud.cyberark.cloud/PasswordVault/API/Platforms/{}"
    )

    def __init__(self, auth, platform_id):
        verify(auth, "PlatformBearer", "auth must be PlatformBearer")
        verify(platform_id, "str", "auth must be str")
        api_path = self._API_PATH_FORMAT.format(auth.token.subdomain, platform_id)
        headers = {
            **auth.header,
            "Content-Type": "application/json"
        }
        method = "GET"
        response = api_call(api_path, method, headers)
        self._response = response.json()


class ExportPlatform(ArkApiCall):
    _API_PATH_FORMAT = (
        "https://{}.privilegecloud.cyberark.cloud/"
        "PasswordVault/API/Platforms/{}/Export/"
    )

    def __init__(self, auth, platform_id):
        verify(auth, "PlatformBearer", "auth must be PlatformBearer")
        verify(platform_id, "str", "auth must be str")
        api_path = self._API_PATH_FORMAT.format(auth.token.subdomain, platform_id)
        headers = {
            **auth.header,
            "Content-Type": "application/json"
        }
        method = "POST"
        response = api_call(
            api_path,
            method,
            headers,
            params={},
            data=b"",
            preload_content=False
        )
        self._response = response
