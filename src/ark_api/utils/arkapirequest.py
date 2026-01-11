from .verify import verify


class ArkApiRequest:
    def __init__(self, url, method, headers, data=b""):
        verify(url, "str", "url must be str")
        verify(method, "str", "method must be str")
        verify(headers, "dict", "headers must be dict")
        verify(data, "bytes", "data must be bytes")
        self._url = url
        self._method = method
        self._headers = headers
        self._data = data

    @property
    def url(self):
        return self._url

    @property
    def method(self):
        return self._method

    @property
    def headers(self):
        return self._headers

    @property
    def data(self):
        return self._data
