from .base_service import BaseService


class ProjectsService(BaseService):
    def __init__(self, api_client):
        super().__init__(api_client)
        self.projects_api_url = "/v2/json/get/projects_2/projects"
        self.competitors_api_url = "/v2/json/get/projects_2/competitors"

    def get_projects(
        self,
        show_site_stat=True,
        show_searchers_and_regions=1,
        include_positions_summary_params=[],
    ):
        """
        Получает список проектов.
        """
        payload = {
            "show_site_stat": show_site_stat,
            "show_searchers_and_regions": show_searchers_and_regions,
            "include_positions_summary_params": include_positions_summary_params,
        }
        endpoint = self.projects_api_url
        return self.send_request(endpoint, payload)

    def get_competitors(self, project_id, only_enabled=False, include_project=False):
        """
        Получает список конкурентов проекта.
        """
        payload = {
            "project_id": project_id,
            "only_enabled": only_enabled,
            "include_project": include_project,
        }
        endpoint = self.competitors_api_url
        return self.send_request(endpoint, payload)

    def get_regions_and_searchers(self, project_id):
        """
        Получает регионы и поисковые системы, привязанные к проекту.
        """
        payload = {
            "project_id": project_id,
            "show_searchers_and_regions": 2,  # Возвращает все регионы
        }
        endpoint = self.projects_api_url
        response = self.send_request(endpoint, payload)
        return response.get("result", {}).get("searchersAndRegions", [])
