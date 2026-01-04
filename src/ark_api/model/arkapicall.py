from abc import ABC, abstractmethod


class ArkApiCall(ABC):
    @abstractmethod
    def __init__(self):
        """
        Following attributes required:
        _response
        """

    @property
    def response(self):
        return self._response
