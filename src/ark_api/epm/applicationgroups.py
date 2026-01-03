from ark_api.model import ArkApiCall
from ark_api.utils import api_call
from ark_api.utils import verify


class ApplicationGroups(ArkApiCall):
    _API_PATH_FORMAT = (
        "{}/EPM/API/{}/Sets/{}/Policies/ApplicationGroups/Search"
    )

    def __init__(self, auth, set_id):
        verify(auth, "EpmBearer", "auth must be EpmBearer")
        verify(set_id, "str", "set_id must be str")
        api_path = self._API_PATH_FORMAT.format(
            auth.token.manager_url,
            auth.token.version,
            set_id
        )
        headers = {**auth.header}
        method = "POST"
        response = api_call(api_path, method, headers)
        self._response = response.json()
