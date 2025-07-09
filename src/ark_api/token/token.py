from ark_api.api import Api, ArkObject
from ark_api.discovery import Discovery
from ark_api.exceptions import ExpiredToken, Unsupported
from ark_api.utils import Secret
from time import time
from platform import system
import jwt
import keyring
import os


class _ArkToken(Api):
    def __init__(self, api_path, username, password):
        assert isinstance(api_path, str), "api_path must be str"
        assert isinstance(username, str), "username must be str"
        assert isinstance(password, Secret), "password must be Secret"
        params = {
            "grant_type": "client_credentials",
            "client_id": username,
            "client_secret": password.use()
        }
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        method = "POST"
        response = self._api_call(headers, params, api_path, method)
        self._access_token = response.access_token
        self._jwt = self._get_unverified_claims(self._access_token)

    @classmethod
    def _get_unverified_claims(cls, access_token):
        _jwt = jwt.decode(
            access_token,
            options={"verify_signature": False}
        )
        return ArkObject(_jwt)

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
        if system() == "Windows":
            if not self._WINDOWS_KEYRING_SUPPORTED:
                raise Unsupported("Windows keyring is not supported")
        service_name = (
            f"{self.__class__.__module__}.{self.__class__.__name__}"
        )
        keyring.set_password(
            service_name=service_name,
            username=self._jwt.unique_name,
            password=self._access_token
        )

    def save_file(self, file):
        with open(file, "w") as token_file:
            token_file.write(self._access_token)

    @classmethod
    def from_string(cls, access_token):
        obj = cls.__new__(cls)
        obj._access_token = access_token
        obj._jwt = obj._get_unverified_claims(obj._access_token)
        if not obj.is_valid():
            raise ExpiredToken("Token has expired")
        return obj

    @classmethod
    def from_keyring(cls, username):
        if system() == "Windows":
            if not cls._WINDOWS_KEYRING_SUPPORTED:
                raise Unsupported("Windows keyring is not supported")
        assert isinstance(username, str), "username must be str"
        access_token = keyring.get_password(
            service_name=f"{cls.__module__}.{cls.__name__}",
            username=username
        )
        if access_token:
            return cls.from_string(access_token)
        else:
            raise LookupError("No keyring found")

    @classmethod
    def from_file(cls, file):
        assert isinstance(file, str), "file must be str"
        if not os.path.exists(file):
            raise FileNotFoundError("Token not found")
        with open(file, "r") as token_file:
            access_token = token_file.read()
        return cls.from_string(access_token)


class Token(_ArkToken):
    _API_PATH_FORMAT = "{}/oauth2/platformtoken"
    _WINDOWS_KEYRING_SUPPORTED = False

    def __init__(self, subdomain, username, password):
        assert isinstance(subdomain, str), "subdomain must be str"
        discovery = Discovery(subdomain)
        api_path = self._API_PATH_FORMAT.format(discovery.endpoint)
        super().__init__(api_path, username, password)


class AppToken(_ArkToken):
    _API_PATH_FORMAT = "{}/oauth2/token/{}"
    _WINDOWS_KEYRING_SUPPORTED = True

    def __init__(self, app_id, subdomain, username, password):
        assert isinstance(app_id, str), "app_id must be str"
        assert isinstance(subdomain, str), "subdomain must be str"
        discovery = Discovery(subdomain)
        api_path = self._API_PATH_FORMAT.format(discovery.endpoint, app_id)
        super().__init__(api_path, username, password)
