from ark_api.api import Api
from ark_api.authorization import Bearer


class SafeMembers(Api):
    _API_PATH_FORMAT = (
        "https://{}.privilegecloud.cyberark.cloud/"
        "PasswordVault/API/Safes/{}/Members/"
    )

    def __init__(self, auth, safe_url_id):
        assert isinstance(auth, Bearer), "auth must be Bearer"
        assert isinstance(safe_url_id, str), "safe_name must be str"
        api_path = self._API_PATH_FORMAT.format(
            auth.token.jwt.subdomain,
            safe_url_id
        )
        params = {"safeUrlId": safe_url_id}
        headers = {
            **auth.header,
            "Content-Type": "application/json"
        }
        method = "GET"
        self._response = self.api_call(api_path, method, headers, params)

    @property
    def value(self):
        return self._response.value
