from .arktoken import ArkToken
from time import time
from base64 import b64decode
import json


class ConjurToken(ArkToken):
    _API_PATH_FORMAT = (
        "https://{}.secretsmgr.cyberark.cloud/api/"
        "authn-oidc/cyberark/conjur/authenticate"
    )

    def __init__(self):
        """
        Following attributes required:
        _response
        """
        res_bytes = self._response.read()
        res_str = res_bytes.decode()
        self._access_token = res_str
        decoded_bytes = b64decode(res_str)
        decoded_str = decoded_bytes.decode()
        decoded = json.loads(decoded_str)
        protected_bytes = b64decode(decoded["protected"])
        protected_str = protected_bytes.decode()
        self._protected = json.loads(protected_str)
        payload_bytes = b64decode(decoded["payload"])
        payload_str = payload_bytes.decode()
        self._payload = json.loads(payload_str)

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
