from .verify import verify
from .logger import Logger
from ark_api.exceptions import APIError
from ark_api import __version__ as ark_api_version
from urllib import request, parse, error
import json


class ApiResponse:
    def __init__(self, response):
        verify(
            response,
            ["HTTPResponse", "HTTPError"],
            "response must be HTTPResponse or HTTPError"
        )
        self._response = response
        self._response_bytes = self._response.read()

    def text(self):
        return self._response_bytes.decode()

    def json(self):
        return json.loads(self.text())

    @property
    def response(self):
        return self._response

    @property
    def response_bytes(self):
        return self._response_bytes


def api_call(api_path, method, headers, params={}, data=b""):
    verify(api_path, "str", "api_path must be str")
    verify(method, "str", "method must be str")
    verify(headers, "dict", "headers must be dict")
    verify(params, "dict", "params must be dict")
    verify(data, "bytes", "data must be bytes")
    headers["User-Agent"] = f"{__name__}/{ark_api_version}"
    if params:
        assert "Content-Type" in headers, "Content-Type required"
        if "x-www-form-urlencoded" in headers["Content-Type"]:
            data = parse.urlencode(params).encode()
        elif "application/json" in headers["Content-Type"]:
            data = json.dumps(params).encode()
    req = request.Request(
        api_path,
        data=data,
        headers=headers,
        method=method
    )
    Logger.log_req(req)
    try:
        _res = request.urlopen(req)
        res = ApiResponse(_res)
        Logger.log_res(res)
        return res
    except error.HTTPError as e:
        res = ApiResponse(e)
        Logger.log_res(res)
        raise APIError(str(e)) from None
    except Exception as e:
        raise APIError(str(e)) from None
