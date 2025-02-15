from .base_service import BaseService
from .payload_factory import PayloadFactory


class KeywordsService(BaseService):

    def __init__(self):
        super().__init__()
        self.endpoint = "/v2/json/get/keywords_2/folders"

    def get_folders(self, project_id, view="tree", show_trash=False):
        payload = PayloadFactory.generate_keywords_payload(
            project_id=project_id, view=view, show_trash=show_trash
        )

        return self.send_request(self.endpoint, payload)
