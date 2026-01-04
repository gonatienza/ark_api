from abc import ABC, abstractmethod


class ArkAuthorization(ABC):
    @abstractmethod
    def __init__(self):
        """
        Following attributes required:
        _header
        """

    @property
    def header(self):
        return self._header
