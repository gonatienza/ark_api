from ark_api.api import Api


_API_PATH_FORMAT = (
    "https://{}.privilegecloud.cyberark.cloud/"
    "api/advanced-settings/ip-allowlist"
)


class GetIpAllowList(Api):
    def __init__(self, token, subdomain):
        assert isinstance(token, str), "token must be Secret"
        assert isinstance(subdomain, str), "subdomain must be str"
        api_path = _API_PATH_FORMAT.format(subdomain)
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        }
        method = "GET"
        params = None
        self._ip_allow_list = self._api_call(
            headers, params, api_path, method
        )

    @property
    def customerPublicIPs(self):
        return self._ip_allow_list.customerPublicIPs

    @property
    def updateInProgress(self):
        return self._ip_allow_list.updateInProgress

    @property
    def lastTaskId(self):
        return self._ip_allow_list.lastTaskId

    @property
    def dateUpdated(self):
        return self._ip_allow_list.dateUpdated


class SetIpAllowList(Api):
    def __init__(self, token, subdomain, ip_allow_list):
        assert isinstance(token, str), "token must be Secret"
        assert isinstance(subdomain, str), "subdomain must be str"
        assert isinstance(ip_allow_list, list), "ip_allow_list must be list"
        api_path = _API_PATH_FORMAT.format(subdomain)
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        }
        method = "PUT"
        params = {'customerPublicIPs': ip_allow_list}
        self._ip_allow_list = self._api_call(
            headers, params, api_path, method
        )

    @property
    def taskId(self):
        return self._ip_allow_list.taskId

    @property
    def status(self):
        return self._ip_allow_list.status
