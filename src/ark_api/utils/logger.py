import logging
import sys
import os


class Logger:
    _DEBUG_ENV_VARIABLE = "ARK_API_DEBUG"
    _DEBUG_ENV_VARIABLE_VALUES = ["1", "true", "yes"]
    _name = __name__
    _logger = logging.getLogger(_name)
    _logger.setLevel(logging.DEBUG)
    _formatter = logging.Formatter(
        f"[{_name}] %(levelname)s: %(message)s"
    )
    _stream_handler = logging.StreamHandler(sys.stdout)
    _stream_handler.setFormatter(_formatter)
    _logger.addHandler(_stream_handler)
    _ark_api_debug = os.getenv(_DEBUG_ENV_VARIABLE, "no")
    _enabled = _ark_api_debug.lower() in _DEBUG_ENV_VARIABLE_VALUES

    @classmethod
    def log_req(cls, req):
        if not cls._enabled:
            return
        cls._logger.debug("[OUTBOUND REQUEST]")
        cls._logger.debug(f"url: {req.url}")
        for header, value in req.headers.items():
            cls._logger.debug(f"header: {header}: {value}")
        cls._logger.debug(f"method: {req.method}")
        cls._logger.debug(f"data: {req.data}")

    @classmethod
    def log_res(cls, res):
        if not cls._enabled:
            return
        cls._logger.debug("[INBOUND RESPONSE]")
        cls._logger.debug(f"code: {res.status} {res.status_msg}")
        headers = {k: v for k, v in res.headers.items()}
        for header, value in headers.items():
            cls._logger.debug(f"header: {header}: {value}")
        cls._logger.debug(f"data: {res.data}")

    @classmethod
    def debug(cls, message):
        if not cls._enabled:
            return
        cls._logger.debug(message)
