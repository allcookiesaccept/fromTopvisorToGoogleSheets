class BaseService:
    def __init__(self, api_client):
        self.api_client = api_client

    def send_request(self, endpoint, payload):
        """
        Отправляет запрос через API-клиент.
        """
        return self.api_client.send_request(endpoint, payload)
