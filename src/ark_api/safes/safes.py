from ark_api.api import Api
from ark_api.utils import Secret


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
        authorization = Secret(f"Bearer {token}")
        headers = {
            "Content-Type": "application/json",
            "Authorization": authorization.use()
        }
        method = "GET"
        self._response = self.api_call(api_path, method, headers, params)

    @property
    def value(self):
        return self._response.value
