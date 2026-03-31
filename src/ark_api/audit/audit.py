from ark_api.model import ArkApiCall
from ark_api.utils import api_call
from ark_api.utils import verify


_API_PATH_FORMAT = "https://{}.audit.cyberark.cloud/api/audits"


class Audit(ArkApiCall):
    _CREATE_QUERY_API_PATH = (
        f"{_API_PATH_FORMAT}/stream/createQuery"
    )
    _RESULTS_API_PATH_FORMAT = (
        f"{_API_PATH_FORMAT}/stream/results"
    )

    def __init__(self, app_auth, api_key_auth, params):
        verify(app_auth, "AppBearer", "auth must be AppBearer")
        verify(api_key_auth, "AuditApiKey", "auth must be AuditApiKey")
        api_path = self._CREATE_QUERY_API_PATH.format(app_auth.token.subdomain)
        headers = {
            **app_auth.header,
            **api_key_auth.header,
            "Content-Type": "application/json"
        }
        method = "POST"
        cursor_ref_res = api_call(api_path, method, headers, params)
        api_path = self._RESULTS_API_PATH_FORMAT.format(app_auth.token.subdomain)
        response = api_call(api_path, method, headers, cursor_ref_res.json())
        self._response = response.json()
