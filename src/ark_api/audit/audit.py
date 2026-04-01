from ark_api.model import ArkApiCall
from ark_api.utils import api_call
from ark_api.utils import verify


class Audit(ArkApiCall):
    _API_PATH_FORMAT = "https://{}.audit.cyberark.cloud/api/audits"
    _CREATE_QUERY_API_PATH = "/stream/createQuery"
    _RESULTS_API_PATH_FORMAT = "/stream/results"

    def __init__(self, app_auth, api_key_auth, params):
        verify(app_auth, "AppBearer", "auth must be AppBearer")
        verify(api_key_auth, "AuditApiKey", "auth must be AuditApiKey")
        self._api_path = self._API_PATH_FORMAT.format(app_auth.token.subdomain)
        self._headers = {
            **app_auth.header,
            **api_key_auth.header,
            "Content-Type": "application/json"
        }
        self._method = "POST"
        api_path = self._api_path + self._CREATE_QUERY_API_PATH
        response = api_call(api_path, self._method, self._headers, params)
        self._cursor_ref = response.json()
        self._response = None

    def _get_events(self):
        api_path = self._api_path + self._RESULTS_API_PATH_FORMAT
        response = api_call(api_path, self._method, self._headers, self._cursor_ref)
        self._response = response.json()

    def is_final_cursor_ref(self):
        if self._response is not None and len(self._response.get("data", [])) == 0:
            return True
        return False

    def get_events(self):
        self._get_events()
        self._cursor_ref = self._response["paging"]["cursor"]
