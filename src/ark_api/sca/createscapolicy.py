from ark_api.api import Api


class CreateScaPolicy(Api):
    _API_PATH_FORMAT = (
        "https://{}.sca.cyberark.cloud/api/policies/create-policy"
    )

    def __init__(self, token, subdomain, params):
        assert isinstance(token, str), "token must be Secret"
        assert isinstance(subdomain, str), "subdomain must be str"
        assert isinstance(params, dict), "params must be dict"
        api_path = self._API_PATH_FORMAT.format(subdomain)
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        }
        method = "POST"
        self._response = self._api_call(headers, params, api_path, method)

    @property
    def job_id(self):
        return self._response.job_id
