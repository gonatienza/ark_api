from ark_api.exceptions import APIError
from ark_api.utils import SecretStr
from abc import ABC, abstractmethod
from urllib import request, parse
from urllib.error import URLError
import json


class EmbeddedObject:
    def __init__(self, attributes):
        assert isinstance(attributes, dict)
        for key, value in attributes.items():
            if isinstance(value, dict):
                setattr(self, key, EmbeddedObject(value))
            else:
                setattr(self, key, value)


class ApiResponse:
    def __init__(self, attributes):
        assert isinstance(attributes, dict)
        for key, value in attributes.items():
            if isinstance(value, dict):
                setattr(self, key, EmbeddedObject(value))
            else:
                setattr(self, key, value)


class Api(ABC):
    @abstractmethod
    def __init__(self):
        pass

    def _api_call(self, headers, params, api_path, method):
        if params:
            if "x-www-form-urlencoded" in headers["Content-Type"]:
                data = parse.urlencode(params).encode()
            elif "application/json" in headers["Content-Type"]:
                data = json.dumps(params).encode()
        else:
            data = b""
        req = request.Request(
            api_path,
            data=data,
            headers=headers,
            method=method
        )
        try:
            res = request.urlopen(req)
            res_bytes = res.read()
            res_str = res_bytes.decode()
            res_dict = json.loads(res_str)
            return ApiResponse(res_dict)
        except URLError as e:
            if params:
                _params = {
                    key: value
                    if not isinstance(value, SecretStr) else "*****"
                    for key, value in params.items()
                }
            else:
                _params = None
            raise APIError(
                f"\nerror: {str(e)}"
                f"\napi_path: '{api_path}'"
                f"\nheaders: {headers}"
                f"\nmethod: '{method}'"
                f"\nparams: {_params}"
            )
        except Exception as e:
            if params:
                _params = {
                    key: value
                    if not isinstance(value, SecretStr) else "*****"
                    for key, value in params.items()
                }
            else:
                _params = None
            raise APIError(
                f"\nerror: {str(e)}"
                f"\nresponse: {e.read().decode()}"
                f"\napi_path: '{api_path}'"
                f"\nheaders: {headers}"
                f"\nmethod: '{method}'"
                f"\nparams: {_params}"
            )
