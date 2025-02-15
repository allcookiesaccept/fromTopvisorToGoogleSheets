from .base_service import BaseService
from .payload_factory import PayloadFactory


class KeywordsService(BaseService):

    def get_folders(self, project_id, view="tree", show_trash=False):
        """
        Получает список папок.
        """
        payload = PayloadFactory.generate_keywords_payload(
            project_id=project_id, view=view, show_trash=show_trash
        )
        endpoint = "/v2/json/get/keywords_2/folders"
        return self.send_request(endpoint, payload)
