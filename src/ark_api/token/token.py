from ark_api.api import Api, ApiResponse
from ark_api.discovery import Discovery
from ark_api.exceptions import ExpiredToken, Unsupported
from ark_api.utils import Secret
from datetime import datetime, timedelta
from platform import system
import keyring
import json
import os


class Token(Api):
    _API_PATH_FORMAT = "{}/oauth2/platformtoken"

    def __init__(self, subdomain, username, password):
        assert isinstance(subdomain, str), "subdomain must be str"
        assert isinstance(username, str), "username must be str"
        assert isinstance(password, Secret), "password must be Secret"
        discovery = Discovery(subdomain)
        api_path = self._API_PATH_FORMAT.format(discovery.endpoint)
        params = {
            "grant_type": "client_credentials",
            "client_id": username,
            "client_secret": password.use()
        }
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        method = "POST"
        self._token = self._api_call(headers, params, api_path, method)
        now_dt = datetime.now()
        delta_dt = timedelta(seconds=self._token.expires_in)
        del self._token.expires_in
        expires_on = now_dt + delta_dt
        self._token.expires_on = expires_on.timestamp()

    def is_valid(self):
        now_dt = datetime.now()
        now = now_dt.timestamp()
        if now > self._token.expires_on:
            return False
        return True

    @property
    def access_token(self):
        return self._token.access_token

    @property
    def expires_on(self):
        return self._token.expires_on

    def _get_json_dict(self):
        json_dict = {
            "access_token": self._token.access_token,
            "expires_on": self._token.expires_on
        }
        return json_dict

    def save_keyring(self, username):
        if system() == "Windows":
            raise Unsupported("Windows keyring is not supported")
        json_dict = self._get_json_dict()
        keyring.set_password(
            service_name=self.__class__.__module__,
            username=username,
            password=json.dumps(json_dict)
        )

    def save_file(self, file):
        json_dict = self._get_json_dict()
        with open(file, "w") as token_file:
            json.dump(json_dict, token_file, indent=4)

    @classmethod
    def _from_json_string(cls, json_str):
        token = ApiResponse(json.loads(json_str))
        if token.expires_on:
            expires_on_dt = datetime.fromtimestamp(token.expires_on)
            now_dt = datetime.now()
            if expires_on_dt < now_dt:
                raise ExpiredToken("Token has expired")
        obj = cls.__new__(cls)
        obj._token = token
        return obj

    @classmethod
    def from_keyring(cls, username):
        if system() == "Windows":
            raise Unsupported("Windows keyring is not supported")
        assert isinstance(username, str), "username must be str"
        json_str = keyring.get_password(
            service_name=cls.__module__,
            username=username
        )
        if json_str:
            return cls._from_json_string(json_str)
        else:
            raise LookupError("No keyring found")

    @classmethod
    def from_file(cls, file):
        assert isinstance(file, str), "file must be str"
        if not os.path.exists(file):
            raise FileNotFoundError("Token not found")
        with open(file, "r") as token_file:
            json_str = token_file.read()
        return cls._from_json_string(json_str)

    @classmethod
    def from_str(cls, access_token):
        assert isinstance(access_token, str), "token must be str"
        json_dict = {
            "access_token": access_token,
            "expires_on": None
        }
        return cls._from_json_string(json.dumps(json_dict))
