from ark_api.api import Api
from ark_api.utils import Secret


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
