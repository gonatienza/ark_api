from .conjurtoken import ConjurToken
from ark_api.utils import verify, SecretBytes
from time import time
from urllib.parse import quote


class ConjurWorkloadToken(ConjurToken):
    _API_PATH_FORMAT = (
        "https://{}.secretsmgr.cyberark.cloud/api/"
        "authn/conjur/{}/authenticate"
    )

    def __init__(self, auth, subdomain, identifier):
        verify(auth, "ConjurApiKey", "auth must be ConjurApiKey")
        verify(subdomain, "str", "subdomain must be str")
        verify(identifier, "str", "identifier must be str")
        self._subdomain = subdomain
        api_path = self._API_PATH_FORMAT.format(
            self._subdomain,
            quote(f"host/{identifier}", safe="")
        )
        headers = {"Accept-Encoding": "base64"}
        data = SecretBytes(auth.api_key.encode())
        method = "POST"
        self._response = self.api_call(
            api_path=api_path,
            method=method,
            headers=headers,
            data=data
        )
        super().__init__()

    @property
    def access_token(self):
        return self._access_token

    @property
    def protected(self):
        return self._protected

    @property
    def payload(self):
        return self._payload

    def is_valid(self):
        now = time()
        if now > self._payload["exp"]:
            return False
        return True
