from .conjurtoken import ConjurToken
from ark_api.utils import verify, api_call
from urllib.parse import quote


class ConjurWorkloadToken(ConjurToken):
    _API_PATH_FORMAT_API_KEY = (
        "https://{}.secretsmgr.cyberark.cloud/api/"
        "authn/conjur/{}/authenticate"
    )
    _API_PATH_FORMAT_AUHTENTICATOR = (
        "https://{}.secretsmgr.cyberark.cloud/api/"
        "authn-jwt/{}/conjur/authenticate"
    )

    def __init__(self, auth, subdomain, identifier, authenticator=""):
        verify(
            auth,
            ["ConjurApiKey", "JwtBearer"],
            "auth must be ConjurApiKey or JwtBearer"
        )
        verify(auth, "JwtBearer", "auth must be JwtBearer")
        verify(subdomain, "str", "subdomain must be str")
        verify(identifier, "str", "identifier must be str")
        verify(authenticator, "str", "authenticator must be str")
        self._subdomain = subdomain
        headers = {"Accept-Encoding": "base64"}
        if auth.__class__.__name__ == "ConjurApiKey":
            api_path = self._API_PATH_FORMAT_API_KEY.format(
                self._subdomain,
                quote(f"host/{identifier}", safe=""),
            )
            data = auth.api_key.get().encode()
            params = {}
        elif auth.__class__.__name__ == "JwtBearer":
            api_path = self._API_PATH_FORMAT_AUHTENTICATOR.format(
                self._subdomain,
                authenticator
            )
            headers.update({"Content-Type": "x-www-form-urlencoded"})
            params = {"jwt": auth.token.access_token.get()}
            data = b""
        method = "POST"
        self._response = api_call(
            api_path=api_path,
            method=method,
            headers=headers,
            params=params,
            data=data
        )
        super().__init__()

    @property
    def subdomain(self):
        return self._subdomain
