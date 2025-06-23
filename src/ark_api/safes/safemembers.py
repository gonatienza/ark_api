from ark_api.api import Api


class SafeMembers(Api):
    _API_PATH_FORMAT = (
        "https://{}.privilegecloud.cyberark.cloud/"
        "PasswordVault/API/Safes/{}/Members/"
    )

    def __init__(self, token, subdomain, safe_url_id):
        assert isinstance(token, str), "token must be str"
        assert isinstance(subdomain, str), "subdomain must be str"
        assert isinstance(safe_url_id, str), "safe_name must be str"
        api_path = self._API_PATH_FORMAT.format(subdomain, safe_url_id)
        params = {"safeUrlId": safe_url_id}
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        }
        method = "GET"
        self._members = self._api_call(headers, params, api_path, method)

    @property
    def value(self):
        return self._members.value
