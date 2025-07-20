from .arkauthorization import ArkAuthorization
from ark_api.utils import Secret, verify
from base64 import b64encode


class Basic(ArkAuthorization):
    def __init__(self, username, password):
        verify(username, "str", "username must be str")
        verify(password, "Secret", "password must be Secret")
        creds = f"{username}:{password.use()}"
        encoded_creds = b64encode(creds.encode())
        authorization = Secret(f"Basic {encoded_creds.decode()}")
        self._header = {"Authorization": authorization.use()}
