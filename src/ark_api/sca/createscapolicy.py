from ark_api.api import Api
from ark_api.authorization import Bearer


class CreateScaPolicy(Api):
    _API_PATH_FORMAT = (
        "https://{}.sca.cyberark.cloud/api/policies/create-policy"
    )

    def __init__(self, auth, params):
        assert isinstance(auth, Bearer), "auth must be Bearer"
        assert isinstance(params, dict), "params must be dict"
        api_path = self._API_PATH_FORMAT.format(auth.token.jwt.subdomain)
        headers = {
            **auth.header,
            "Content-Type": "application/json"
        }
        method = "POST"
        self._response = self.api_call(api_path, method, headers, params)

    @property
    def job_id(self):
        return self._response.job_id
