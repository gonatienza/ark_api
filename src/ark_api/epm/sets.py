from ark_api.model import ArkApiCall
from ark_api.utils import api_call
from ark_api.utils import verify


class Sets(ArkApiCall):
    _API_PATH_FORMAT = "{}/EPM/API/{}/Sets"

    def __init__(self, auth):
        verify(auth, "EpmBearer", "auth must be EpmBearer")
        api_path = self._API_PATH_FORMAT.format(
            auth.token.manager_url,
            auth.token.version
        )
        headers = {**auth.header}
        method = "GET"
        response = api_call(api_path, method, headers)
        self._response = response.json()
