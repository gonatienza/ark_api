from ark_api.api import Api
from ark_api.utils import ArkObject
from ark_api.exceptions import ExpiredToken
from abc import abstractmethod
from time import time
import keyring
import jwt
import os


class ArkToken(Api):
    @abstractmethod
    def __init__(self):
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
    def access_token(self):
        return self._access_token

    @property
    def jwt(self):
        return self._jwt

    def save_keyring(self):
        service_name = (
            f"{self.__class__.__module__}.{self.__class__.__name__}"
        )
        keyring.set_password(
            service_name=service_name,
            username=self._jwt.unique_name,
            password=self._access_token
        )

    def save_file(self, file):
        assert isinstance(file, str), "file must be str"
        with open(file, "w") as token_file:
            token_file.write(self._access_token)

    @classmethod
    def _from_string(cls, access_token):
        obj = cls.__new__(cls)
        obj._access_token = access_token
        obj._jwt = obj._get_unverified_claims(obj._access_token)
        if not obj.is_valid():
            raise ExpiredToken("Token has expired")
        return obj

    @classmethod
    def from_keyring(cls, username):
        assert isinstance(username, str), "username must be str"
        access_token = keyring.get_password(
            service_name=f"{cls.__module__}.{cls.__name__}",
            username=username
        )
        if access_token:
            return cls._from_string(access_token)
        else:
            raise LookupError("No keyring found")

    @classmethod
    def from_file(cls, file):
        assert isinstance(file, str), "file must be str"
        if not os.path.exists(file):
            raise FileNotFoundError("Token not found")
        with open(file, "r") as token_file:
            access_token = token_file.read()
        return cls._from_string(access_token)
