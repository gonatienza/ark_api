from ark_api.api import Api


class Safes(Api):
    _API_PATH_FORMAT = (
        "https://{}.privilegecloud.cyberark.cloud/PasswordVault/API/Safes/"
    )

    def __init__(self, token, subdomain):
        assert isinstance(token, str), "token must be str"
        assert isinstance(subdomain, str), "subdomain must be str"
        api_path = self._API_PATH_FORMAT.format(subdomain)
        params = {
            "includeAccounts": True,
            "extendedDetails": True
        }
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        }
        method = "GET"
        self._response = self._api_call(headers, params, api_path, method)

    @property
    def value(self):
        return self._response.value
