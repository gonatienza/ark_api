from .verify import verify
from .arkapiclient import ArkApiClient
from urllib.parse import urlencode
import json


def api_call(api_path, method, headers, params={}, data=b""):
    verify(api_path, "str", "api_path must be str")
    verify(method, "str", "method must be str")
    verify(headers, "dict", "headers must be dict")
    verify(params, "dict", "params must be dict")
    verify(data, "bytes", "data must be bytes")
    if params:
        if "Content-Type" not in headers:
            raise ValueError("Content-Type required")
        if "x-www-form-urlencoded" in headers["Content-Type"]:
            data = urlencode(params).encode()
        elif "application/json" in headers["Content-Type"]:
            data = json.dumps(params).encode()
    return ArkApiClient.call(api_path, method, headers, data)
