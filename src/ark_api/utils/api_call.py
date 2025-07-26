from ark_api.exceptions import APIError
from ark_api.utils import (
    mask_secrets_from_dict,
    mask_secrets_from_bytes,
    verify
)
from urllib import request, parse
import json


class ApiResponse:
    def __init__(self, response):
        verify(response, "HTTPResponse", "response must be HTTPResponse")
        self._response = response
        self._response_bytes = self._response.read()

    def text(self):
        return self._response_bytes.decode()

    def json(self):
        return json.loads(self.text())


def api_call(api_path, method, headers, params={}, data=b""):
    verify(api_path, "str", "api_path must be str")
    verify(method, "str", "method must be str")
    verify(headers, "dict", "headers must be dict")
    verify(params, "dict", "params must be dict")
    verify(data, "bytes", "data must be bytes")
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
    try:
        return ApiResponse(request.urlopen(req))
    except Exception as e:
        if params:
            _params = mask_secrets_from_dict(params)
        else:
            _params = None
        if data:
            _data = mask_secrets_from_bytes(data)
        else:
            _data = None
        _headers = mask_secrets_from_dict(headers)
        message_list = [
            f"error: {str(e)}",
            f"api_path: '{api_path}'",
            f"headers: {_headers}",
            f"method: '{method}'",
            f"params: {_params}",
            f"data: {_data}"
        ]
        if hasattr(e, "read"):
            try:
                response = e.read().decode()
            except Exception:
                response = "<unreadable>"
            message_list.append(f"response: {response}")
        raise APIError("\n".join(message_list))
