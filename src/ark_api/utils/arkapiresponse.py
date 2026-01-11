from .verify import verify


class ArkApiResponse:
    def __init__(self, response):
        verify(response, "HTTPResponse", "response must be HTTPResponse")
        self._response = response

    def is_ok(self):
        if 200 <= self.status <= 399:
            return True
        else:
            return False

    def text(self):
        return self._response.data.decode()

    def json(self):
        return self._response.json()

    @property
    def status(self):
        return self._response.status

    @property
    def status_msg(self):
        return self._response.reason

    @property
    def headers(self):
        return self._response.headers

    @property
    def data(self):
        return self._response.data

    @property
    def ok(self):
        return self._ok
