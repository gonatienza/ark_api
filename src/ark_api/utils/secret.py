class _SecretReprMixin:
    def __repr__(self):
        return f"{self.__class__.__name__}('***')"


class SecretStr(_SecretReprMixin, str):
    def __str__(self):
        return super().__str__()

    def get(self):
        return super().__str__()


class SecretBytes(_SecretReprMixin, bytes):
    def get(self):
        return super().__bytes__()


class Secret:
    def __init__(self, value):
        assert isinstance(value, (str, bytes)), "value must be str or bytes"
        if isinstance(value, str):
            self._secret = SecretStr(value)
        elif isinstance(value, bytes):
            self._secret = SecretBytes(value)

    def get(self):
        return self._secret.get()
