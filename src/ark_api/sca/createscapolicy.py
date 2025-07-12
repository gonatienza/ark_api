from ark_api.api import Api
from ark_api.utils import Secret


class CreateScaPolicy(Api):
    _API_PATH_FORMAT = (
        "https://{}.sca.cyberark.cloud/api/policies/create-policy"
    )

    def __init__(self, token, subdomain, params):
        assert isinstance(token, Secret), "token must be Secret"
        assert isinstance(subdomain, str), "subdomain must be str"
        assert isinstance(params, dict), "params must be dict"
        api_path = self._API_PATH_FORMAT.format(subdomain)
        authorization = Secret(f"Bearer {token.use()}")
        headers = {
            "Content-Type": "application/json",
            "Authorization": authorization.use()
        }
        method = "POST"
        self._response = self.api_call(api_path, method, headers, params)

    @property
    def job_id(self):
        return self._response.job_id
