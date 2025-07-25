from ark_api.exceptions import APIError
from ark_api.utils import (
    ArkObject,
    mask_secrets_from_dict,
    mask_secrets_from_bytes,
    verify
)
from abc import ABC, abstractmethod
from urllib import request, parse
import json


class Api(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @classmethod
    def json_api_call(cls, api_path, method, headers, params={}):
        response = cls.api_call(api_path, method, headers, params)
        response_bytes = response.read()
        response_str = response_bytes.decode()
        response_dict = json.loads(response_str)
        return ArkObject(response_dict)

    @staticmethod
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
            res = request.urlopen(req)
            return res
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
