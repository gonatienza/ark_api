from .logger import Logger
from .verify import verify
from .arkapirequest import ArkApiRequest
from .arkapiresponse import ArkApiResponse
from ark_api import __version__ as ark_api_version
from ark_api.exceptions import ArkApiClientError
from urllib3 import PoolManager, Timeout


class ArkApiClient:
    http = PoolManager()

    @classmethod
    def call(cls, api_path, method, headers, data):
        verify(api_path, "str", "api_path must be str")
        verify(method, "str", "method must be str")
        verify(headers, "dict", "headers must be dict")
        verify(data, "bytes", "data must be bytes")
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
                timeout=Timeout(connect=5.0, read=10.0)
            )
            res = ArkApiResponse(_res)
            Logger.log_res(res)
        except Exception as e:
            raise ArkApiClientError(str(e)) from None
        if res.is_ok():
            return res
        else:
            raise ArkApiClientError(f"{res.status} - {res.status_msg}")
