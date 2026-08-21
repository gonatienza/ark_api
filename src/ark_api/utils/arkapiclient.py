from .logger import Logger
from .verify import verify
from .arkapirequest import ArkApiRequest
from .arkapiresponse import ArkApiResponse
from ark_api import __version__ as ark_api_version
from ark_api.exceptions import ArkApiClientError
from urllib3 import PoolManager, Timeout
import os

class ArkApiClient:
    _VERIFY_CERT_ENV_VARIABLE = "ARK_VERIFY_CERT"
    _VERIFY_CERT_ENV_VARIABLE_DISABLED = ["0", "false", "no"]
    _verify_cert = os.getenv(_VERIFY_CERT_ENV_VARIABLE, "yes")
    _verify_cert_disabled = _verify_cert.lower() in _VERIFY_CERT_ENV_VARIABLE_DISABLED
    if _verify_cert_disabled:
        http = PoolManager(cert_reqs="CERT_NONE", assert_hostname=False)
    else:
        http = PoolManager()

    @classmethod
    def call(cls, api_path, method, headers, data, **kwargs):
        verify(api_path, "str", "api_path must be str")
        verify(method, "str", "method must be str")
        verify(headers, "dict", "headers must be dict")
        verify(data, "bytes", "data must be bytes")
        verify(kwargs, "dict", "kwargs must be dict")
        headers["User-Agent"] = f"{__name__}/{ark_api_version}"
        req = ArkApiRequest(
            url=api_path,
            data=data,
            headers=headers,
            method=method
        )
        Logger.log_req(req)
        try:
            _res = cls.http.request(
                method=req.method,
                url=req.url,
                body=req.data,
                headers=req.headers,
                timeout=Timeout(connect=5.0, read=10.0),
                **kwargs
            )
            res = ArkApiResponse(_res)
            Logger.log_res(res)
        except Exception as e:
            raise ArkApiClientError(str(e)) from None
        if not res.is_ok():
            raise ArkApiClientError(f"{res.status} - {res.status_msg}")
        return res
