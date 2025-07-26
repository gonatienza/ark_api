from .conjurtoken import ConjurToken
from ark_api.utils import verify


class ConjurIdToken(ConjurToken):
    _API_PATH_FORMAT = (
        "https://{}.secretsmgr.cyberark.cloud/api/"
        "authn-oidc/cyberark/conjur/authenticate"
    )

    def __init__(self, auth):
        verify(auth, "Bearer", "auth must be Bearer")
        api_path = self._API_PATH_FORMAT.format(auth.token.subdomain)
        params = {"id_token": auth.token.access_token.get()}
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept-Encoding": "base64"
        }
        method = "POST"
        self._subdomain = auth.token.subdomain
        self._response = self.api_call(api_path, method, headers, params)
        super().__init__()
