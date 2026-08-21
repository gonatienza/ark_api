from .conjurtoken import ConjurToken
from ark_api.utils import verify, api_call
from urllib.parse import quote


class ConjurWorkloadToken(ConjurToken):
    _API_PATH_FORMAT_API_KEY = (
        "https://{}/api/authn/conjur/{}/authenticate"
    )
    _API_PATH_FORMAT_AUHTENTICATOR = (
        "https://{}/api/authn-jwt/{}/conjur/authenticate"
    )

    def __init__(self, auth, endpoint, identifier, authenticator=""):
        verify(
            auth,
            ["ConjurApiKey", "JwtBearer"],
            "auth must be ConjurApiKey or JwtBearer"
        )
        verify(endpoint, "str", "endpoint must be str")
        verify(identifier, "str", "identifier must be str")
        verify(authenticator, "str", "authenticator must be str")
        self._endpoint = endpoint
        headers = {"Accept-Encoding": "base64"}
        if auth.__class__.__name__ == "ConjurApiKey":
            api_path = self._API_PATH_FORMAT_API_KEY.format(
                self._endpoint,
                quote(f"host/{identifier}", safe=""),
            )
            data = auth.api_key.get().encode()
            params = {}
        elif auth.__class__.__name__ == "JwtBearer":
            api_path = self._API_PATH_FORMAT_AUHTENTICATOR.format(
                self._endpoint,
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
