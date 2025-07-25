from .arktoken import ArkToken
from ark_api.utils import ArkObject, verify
from abc import abstractmethod
from time import time
import keyring
import jwt
import os
import json


class JwtToken(ArkToken):
    @abstractmethod
    def __init__(self):
        """
        Following attributes required:
        _access_token
        _subdomain
        _jwt
        """
        pass

    @staticmethod
    def _get_unverified_claims(_jwt):
        _jwt_dict = jwt.decode(
            _jwt,
            options={"verify_signature": False}
        )
        return ArkObject(_jwt_dict)

    def is_valid(self):
        now = time()
        if now > self._jwt.exp:
            return False
        return True

    @property
    def jwt(self):
        return self._jwt

    def encode(self):
        ret = {
            "access_token": self._access_token,
            "subdomain": self._subdomain
        }
        return json.dumps(ret)

    def save_keyring(self):
        service_name = (
            f"{self.__class__.__module__}.{self.__class__.__name__}"
        )
        keyring.set_password(
            service_name=service_name,
            username=self._jwt.unique_name,
            password=self.encode()
        )

    def save_file(self, file):
        verify(file, "str", "file must be str")
        with open(file, "w") as token_file:
            token_file.write(self.encode())

    @classmethod
    def from_string(cls, token_str):
        verify(token_str, "str", "token_str must be str")
        obj = cls.__new__(cls)
        token = json.loads(token_str)
        obj._subdomain = token["subdomain"]
        obj._access_token = token["access_token"]
        obj._jwt = obj._get_unverified_claims(obj._access_token)
        return obj

    @classmethod
    def from_keyring(cls, username):
        verify(username, "str", "username must be str")
        token_str = keyring.get_password(
            service_name=f"{cls.__module__}.{cls.__name__}",
            username=username
        )
        if token_str:
            return cls.from_string(token_str)
        else:
            raise LookupError("No keyring found")

    @classmethod
    def from_file(cls, file):
        verify(file, "str", "file must be str")
        if not os.path.exists(file):
            raise FileNotFoundError("Token not found")
        with open(file, "r") as token_file:
            token_str = token_file.read()
        return cls.from_string(token_str)
