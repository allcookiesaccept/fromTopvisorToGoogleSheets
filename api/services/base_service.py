from abc import ABC


class BaseService(ABC):
    def __init__(self, api_client):
        super().__init__()
        self.api_client = api_client

    def send_request(self, endpoint, payload):

        return self.api_client.send_request(endpoint, payload)
