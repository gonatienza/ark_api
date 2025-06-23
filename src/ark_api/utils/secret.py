from ark_api.exceptions import SecretUsed


class Secret:
    def __init__(self, value):
        self._value = SecretStr.from_str(value)
        self._used = False

    def use(self):
        if not self._used:
            ret = self._value
            self._value = None
            self._used = True
            return ret
        else:
            raise SecretUsed


class SecretStr(str):
    @classmethod
    def from_str(cls, value):
        assert isinstance(value, str)
        return cls(value)
