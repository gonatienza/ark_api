from ark_api.api import Api
from abc import abstractmethod


class ArkToken(Api):
    @abstractmethod
    def __init__(self):
        """
        Following attributes required:
        _subdomain
        _access_token
        """
        pass

    @property
    def subdomain(self):
        return self._subdomain

    @property
    def access_token(self):
        return self._access_token
