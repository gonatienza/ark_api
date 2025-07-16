from abc import ABC, abstractmethod


class ArkAuthorization(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @property
    def header(self):
        return self._header
