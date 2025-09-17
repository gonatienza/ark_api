from .arktoken import ArkToken
from ark_api.utils import verify, Secret
from time import time
import jwt


class JwtToken(ArkToken):
    def __init__(self):
        """
        Following attributes required:
        _access_token
        _jwt
        """
        pass

    @staticmethod
    def _get_unverified_claims(_jwt):
        _jwt_dict = jwt.decode(
            _jwt,
            options={"verify_signature": False}
        )
        return _jwt_dict

    def is_valid(self):
        now = time()
        if now > self._jwt["exp"]:
            return False
        return True

    @property
    def jwt(self):
        return self._jwt

    @classmethod
    def from_string(cls, token_str):
        verify(token_str, "str", "token_str must be str")
        obj = cls.__new__(cls)
        obj._access_token = Secret(token_str)
        obj._jwt = obj._get_unverified_claims(obj._access_token.get())
        return obj
