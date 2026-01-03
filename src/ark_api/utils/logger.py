import logging
import json
import sys
import os


class Logger:
    _DEBUG_ENV_VARIABLE = "ARK_API_LOGGING"
    _DEBUG_ENV_VARIABLE_VALUES = {"debug": logging.DEBUG}
    _name = __name__
    _logger = logging.getLogger(_name)
    _ark_api_logging = os.getenv(_DEBUG_ENV_VARIABLE)
    if _ark_api_logging in _DEBUG_ENV_VARIABLE_VALUES:
        level = _DEBUG_ENV_VARIABLE_VALUES[_ark_api_logging]
    else:
        level = logging.INFO
    _logger.setLevel(level)
    _formatter = logging.Formatter(
        f"[{_name}] %(levelname)s: %(message)s"
    )
    _stream_handler = logging.StreamHandler(sys.stdout)
    _stream_handler.setFormatter(_formatter)
    _logger.addHandler(_stream_handler)

    @classmethod
    def debug_out_req(cls, req):
        message = (
            "[OUTBOUND REQUEST] ->\n"
            f"api_path: '{req.full_url}'\n"
            f"headers: {json.dumps(req.headers, indent=4)}\n"
            f"method: {req.method}\n"
            f"data: {req.data}"
        )
        cls._logger.debug(message)

    @classmethod
    def debug_in_res(cls, res):
        headers = {k: v for k, v in res.response.headers.items()}
        message = (
            "[INBOUND RESPONSE] ->\n"
            f"code: {res.response.code} {res.response.msg}\n"
            f"headers: {json.dumps(headers, indent=4)}\n"
            f"data: {res.response_bytes}"
        )
        cls._logger.debug(message)

    @classmethod
    def debug(cls, message):
        return cls._logger.debug(message)
