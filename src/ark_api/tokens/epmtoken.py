from .arktoken import ArkToken
from ark_api.utils import verify, Secret, api_call


class EpmToken(ArkToken):
    _API_PATH_FORMAT = "https://{}/EPM/API/{}/Auth/EPM/Logon"

    def __init__(self, dispatcher, version, username, password):
        verify(dispatcher, "str", "subdomain must be str")
        verify(version, "str", "version must be str")
        verify(username, "str", "username must be str")
        verify(password, "Secret", "password must be Secret")
        self._version = version
        api_path = self._API_PATH_FORMAT.format(dispatcher, self._version)
        params = {
            "Username": username,
            "Password": password.get(),
            "ApplicationID": self.__class__.__name__
        }
        headers = {"Content-Type": "application/json"}
        method = "POST"
        response = api_call(api_path, method, headers, params)
        self._response = response.json()
        self._access_token = Secret(self._response["EPMAuthenticationResult"])
        self._manager_url = self._response["ManagerURL"]

    @property
    def manager_url(self):
        return self._manager_url

    @property
    def version(self):
        return self._version
