from ark_api.api import Api
from ark_api.utils import verify


_API_PATH_FORMAT = (
    "https://{}.privilegecloud.cyberark.cloud/"
    "api/advanced-settings/ip-allowlist"
)


class GetIpAllowList(Api):
    def __init__(self, auth):
        verify(auth, "PlatformBearer", "auth must be PlatformBearer")
        api_path = _API_PATH_FORMAT.format(auth.token.subdomain)
        headers = {
            **auth.header,
            "Content-Type": "application/json"
        }
        method = "GET"
        self._response = self.json_api_call(api_path, method, headers)


class SetIpAllowList(Api):
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
        self._response = self.json_api_call(api_path, method, headers, params)
