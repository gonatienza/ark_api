from ark_api.model import ArkApiCall
from ark_api.utils import api_call
from ark_api.utils import verify


_API_PATH_FORMAT = (
    "https://{}.privilegecloud.cyberark.cloud/"
    "api/advanced-settings/ip-allowlist"
)


class GetIpAllowList(ArkApiCall):
    def __init__(self, auth):
        verify(auth, "PlatformBearer", "auth must be PlatformBearer")
        api_path = _API_PATH_FORMAT.format(auth.token.subdomain)
        headers = {
            **auth.header,
            "Content-Type": "application/json"
        }
        method = "GET"
        response = api_call(api_path, method, headers)
        self._response = response.json()


class SetIpAllowList(ArkApiCall):
    def __init__(self, auth, ip_allow_list):
        verify(auth, "PlatformBearer", "auth must be PlatformBearer")
        verify(ip_allow_list, "list", "ip_allow_list must be list")
        api_path = _API_PATH_FORMAT.format(auth.token.subdomain)
        headers = {
            **auth.header,
            "Content-Type": "application/json"
        }
        method = "PUT"
        params = {'customerPublicIPs': ip_allow_list}
        response = api_call(api_path, method, headers, params)
        self._response = response.json()
