from abc import abstractmethod
from ark_api.model import ArkApiCall


class ArkToken(ArkApiCall):
    @abstractmethod
    def __init__(self):
        """
        Following attributes required:
        _access_token
        """
        pass

    @property
    def subdomain(self):
        return self._subdomain

    @property
    def access_token(self):
        return self._access_token
