from ark_api.utils import verify, api_call
from ark_api.model import ArkApiCall
from ark_api.discovery import Discovery
from ark_api.exceptions import ArkApiError
from ark_api.tokens import PlatformToken


class Authentication(ArkApiCall):
    _API_PATH_FORMAT_START = "{}/Security/StartAuthentication"
    _API_PATH_FORMAT_ADVANCE = "{}/Security/AdvanceAuthentication"

    def __init__(self, subdomain, username):
        verify(subdomain, "str", "subdomain must be str")
        verify(username, "str", "username must be str")
        self._subdomain = subdomain
        discovery = Discovery(self._subdomain)
        self._start_api_path = self._API_PATH_FORMAT_START.format(
            discovery.response["endpoint"]
        )
        self._advance_api_path = self._API_PATH_FORMAT_ADVANCE.format(
            discovery.response["endpoint"]
        )
        params = {"Version": "1.0", "User": username}
        self._headers = {"Content-Type": "application/json"}
        self._method = "POST"
        response = api_call(
            self._start_api_path, self._method, self._headers, params
        )
        self._response = response.json()
        if not self._response["success"]:
            raise ArkApiError(self._response["Message"])
        if "IdpRedirectUrl" in self._response["Result"]:
            redirect_url = self._response["Result"]["IdpRedirectUrl"]
            raise ArkApiError(
                f"received redirect to external IdP: {redirect_url}"
            )
        self._responses = [self._response]
        self._session_id = self._response["Result"]["SessionId"]
        self._challenges = self._response["Result"]["Challenges"]
        self._advance_params = {}
        self._token = None
        self._terminated = False

    @property
    def responses(self):
        return self._responses

    @property
    def session_id(self):
        return self._session_id

    @property
    def challenges(self):
        return self._challenges

    @property
    def token(self):
        return self._token

    @property
    def terminated(self):
        return self._terminated

    def requires_mfa(self):
        if len(self._challenges) > 1:
            return True
        else:
            return False

    def get_mechanisms(self, challenge_index):
        verify(challenge_index, "int", "index must be int")
        return self._challenges[challenge_index]["Mechanisms"]

    def _raise_if_terminated(self):
        if self._terminated:
            raise ArkApiError("authentication was terminated")

    def _update_advance_params(self, response):
        if not self._advance_params:
            self._advance_params = {"SessionId": self._session_id}
            self._advance_params.update(response)
        elif "MultipleOperations" not in self._advance_params:
            del self._advance_params["SessionId"]
            self._advance_params = {
                "SessionId": self._session_id,
                "MultipleOperations": [self._advance_params]
            }
        if "MultipleOperations" not in self._advance_params:
            self._advance_params.update(response)
        else:
            self._advance_params["MultipleOperations"].append(response)

    def add_answer(self, challenge_index, mechanism_index, answer):
        self._raise_if_terminated()
        verify(challenge_index, "int", "challenge_index must be int")
        verify(mechanism_index, "int", "mechanism_index must be int")
        verify(answer, "Secret", "answer must be Secret")
        challenge = self._challenges[challenge_index]
        mechanism = challenge["Mechanisms"][mechanism_index]
        response = {
            "MechanismId": mechanism["MechanismId"],
            "Answer": answer.get(),
            "Action": "Answer"
        }
        self._update_advance_params(response)

    def add_oob(self, challenge_index, mechanism_index):
        self._raise_if_terminated()
        verify(challenge_index, "int", "challenge_index must be int")
        verify(mechanism_index, "int", "mechanism_index must be int")
        challenge = self._challenges[challenge_index]
        mechanism = challenge["Mechanisms"][mechanism_index]
        oob = {
            "MechanismId": mechanism["MechanismId"],
            "Action": "StartOOB"
        }
        self._update_advance_params(oob)

    def advance(self):
        self._raise_if_terminated()
        _params = self._advance_params
        _response = api_call(
            self._advance_api_path,
            self._method,
            self._headers,
            _params
        )
        response = _response.json()
        if not response["success"]:
            self._terminated = True
            raise ArkApiError(response["Message"])
        self._advance_params = {}
        self._response = response
        self._responses.insert(0, self._response)
        if "Token" in self._response["Result"]:
            self._token = PlatformToken.from_string(
                self._subdomain, self._response["Result"]["Token"]
            )
            self._terminated = True

    def poll(self, challenge_index, mechanism_index):
        self._raise_if_terminated()
        verify(challenge_index, "int", "challenge_index must be int")
        verify(mechanism_index, "int", "mechanism_index must be int")
        challenge = self._challenges[challenge_index]
        mechanism = challenge["Mechanisms"][mechanism_index]
        self._advance_params = {
            "Action": "Poll",
            "SessionId": self._session_id,
            "MechanismId": mechanism["MechanismId"]
        }
        self.advance()
