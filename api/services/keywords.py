from .base_service import BaseService
from .payload_factory import PayloadFactory


class KeywordsService(BaseService):
    def __init__(self, api_client):
        super().__init__(api_client)
        self.folders_endpoint = "/v2/json/get/keywords_2/folders"
        self.groups_endpoint = "/v2/json/get/keywords_2/groups"
        self.volume_endpoint = "/v2/json/get/keywords_2/volume"

    def get_folders(self, project_id, view="tree", show_trash=False):
        payload = PayloadFactory.generate_keywords_get_folders_payload(
            project_id=project_id, view=view, show_trash=show_trash
        )
        return self.send_request(self.folders_endpoint, payload)

    def get_groups(self, project_id, folder_id=None, show_trash=False):
        payload = PayloadFactory.generate_keywords_get_groups_payload(
            project_id=project_id, view="list", show_trash=show_trash
        )
        if folder_id:
            payload["folder_id"] = folder_id
        return self.send_request(self.groups_endpoint, payload)

    def get_volume(self, project_id, qualifiers, target_type="groups", filters=None):
        payload = PayloadFactory.generate_keywords_get_volume_payload(
            project_id=project_id,
            qualifiers=qualifiers,
            target_type=target_type,
            filters=filters,
        )
        return self.send_request(self.volume_endpoint, payload)
