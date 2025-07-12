from ark_api.api import Api
from .flowauthentication import FlowAuthentication
from urllib.parse import urlparse


class Flow(Api):
    _PLAY_PATH = "play"
    _STOP_PATH = "stop"
    _STATUS_PATH = "status"

    def __init__(self, flow_url, flow_authentication):
        assert isinstance(flow_url, str), "flow_url must be str"
        assert isinstance(flow_authentication, FlowAuthentication), (
            "flow_authentication must be FlowAuthentication"
        )
        self._flow_authentication = flow_authentication
        self._play_flow_url = flow_url
        parsed = urlparse(self._play_flow_url)
        parsed_path_parts = parsed.path.split("/")
        base_flow_parts = parsed_path_parts[:-1]
        flows_parts = parsed_path_parts[:-2]
        base_flow_path = "/".join(base_flow_parts)
        flows_path = "/".join(flows_parts)
        self._flows_url = f"{parsed.scheme}://{parsed.netloc}{flows_path}"
        self._flow_url = (
            f"{parsed.scheme}://{parsed.netloc}{base_flow_path}"
        )
        self._run_id = None
        self._started = False

    @property
    def run_id(self):
        return self._run_id

    def _call_flow(self, url):
        return self.api_call(
            url,
            "GET",
            self._flow_authentication.headers,
            None
        )

    def play(self):
        url = f"{self._flow_url}/{self._PLAY_PATH}"
        response = self._call_flow(url)
        self._run_id = response.run_id
        self._started = True
        return response

    def status(self):
        if self._started:
            url = f"{self._flow_url}/{self._run_id}/{self._STATUS_PATH}"
            response = self._call_flow(url)
            return response.status
        else:
            raise RuntimeError(
                f"No running job id. Must call "
                f"{self.__class__.__name__}.play() first"
            )

    def stop(self):
        status = self.status()
        if status == 'running':
            url = f"{self._flows_url}/{self._run_id}/{self._STOP_PATH}"
            return self._call_flow(url)
        else:
            raise RuntimeError(f"Invalid job status: '{status}'")
