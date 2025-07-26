from ark_api.model import ArkApiCall
from ark_api.utils import api_call
from ark_api.utils import verify


class CreateScaPolicy(ArkApiCall):
    _API_PATH_FORMAT = (
        "https://{}.sca.cyberark.cloud/api/policies/create-policy"
    )

    def __init__(self, auth, params):
        verify(auth, "PlatformBearer", "auth must be PlatformBearer")
        verify(params, "dict", "params must be dict")
        api_path = self._API_PATH_FORMAT.format(auth.token.subdomain)
        headers = {
            **auth.header,
            "Content-Type": "application/json"
        }
        method = "POST"
        response = api_call(api_path, method, headers, params)
        self._response = response.json()
