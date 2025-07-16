from ark_api.exceptions import APIError
from ark_api.utils import ArkObject, mask_secrets_from_dict
from abc import ABC, abstractmethod
from urllib import request, parse
import json


class Api(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @classmethod
    def api_call(cls, api_path, method, headers, params):
        res = cls._api_call(api_path, method, headers, params)
        res_bytes = res.read()
        res_str = res_bytes.decode()
        res_dict = json.loads(res_str)
        return ArkObject(res_dict)

    @staticmethod
    def _api_call(api_path, method, headers, params):
        if params:
            assert "Content-Type" in headers, "Content-Type required"
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
            return res
        except Exception as e:
            if params:
                _params = mask_secrets_from_dict(params)
            else:
                _params = None
            _headers = mask_secrets_from_dict(headers)
            message_list = [
                f"error: {str(e)}",
                f"api_path: '{api_path}'",
                f"headers: {_headers}",
                f"method: '{method}'",
                f"params: {_params}"
            ]
            if hasattr(e, "read"):
                try:
                    response = e.read().decode()
                except Exception:
                    response = "<unreadable>"
                message_list.append(f"response: {response}")
            raise APIError("\n".join(message_list))
