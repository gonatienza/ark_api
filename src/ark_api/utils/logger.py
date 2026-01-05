import logging
import sys
import os


class Logger:
    _DEBUG_ENV_VARIABLE = "ARK_API_LOGGING"
    _DEBUG_ENV_VARIABLE_VALUES = {
        "error": logging.ERROR,
        "info": logging.INFO,
        "debug": logging.DEBUG
    }
    _name = __name__
    _logger = logging.getLogger(_name)
    _ark_api_logging = os.getenv(_DEBUG_ENV_VARIABLE)
    if _ark_api_logging in _DEBUG_ENV_VARIABLE_VALUES:
        _level = _DEBUG_ENV_VARIABLE_VALUES[_ark_api_logging]
    else:
        _level = logging.ERROR
    _logger.setLevel(_level)
    _formatter = logging.Formatter(
        f"[{_name}] %(levelname)s: %(message)s"
    )
    _stream_handler = logging.StreamHandler(sys.stdout)
    _stream_handler.setFormatter(_formatter)
    _logger.addHandler(_stream_handler)

    @classmethod
    def log_req(cls, req):
        cls._logger.info("[OUTBOUND REQUEST] ->")
        cls._logger.info(f"api_path: {req.full_url}")
        for header, value in req.headers.items():
            cls._logger.info(f"header: {header}: {value}")
        cls._logger.info(f"method: {req.method}")
        cls._logger.debug(f"data: {req.data}")

    @classmethod
    def log_res(cls, res):
        cls._logger.info("[INBOUND RESPONSE] ->")
        cls._logger.info(f"code: {res.response.code} {res.response.msg}")
        headers = {k: v for k, v in res.response.headers.items()}
        for header, value in headers.items():
            cls._logger.info(f"header: {header}: {value}")
        cls._logger.debug(f"data: {res.response_bytes}")

    @classmethod
    def error(cls, message):
        return cls._logger.error(message)

    @classmethod
    def info(cls, message):
        return cls._logger.info(message)

    @classmethod
    def debug(cls, message):
        return cls._logger.debug(message)
