import requests
from config.logger import logger


class TopvisorAPI:
    def __init__(self, user_id, api_key):
        self.base_url = "https://api.topvisor.com"
        self.headers = {
            "Content-type": "application/json",
            "User-Id": user_id,
            "Authorization": f"bearer {api_key}",
        }

    def send_request(self, endpoint, payload):
        """
        Отправляет POST-запрос к API Topvisor.
        """
        try:
            url = f"{self.base_url}{endpoint}"
            response = requests.post(url, headers=self.headers, json=payload)
            response.raise_for_status()
            logger.debug(f"Запрос к API выполнен успешно: {url}")
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Ошибка при запросе к API: {e}")
            raise


from .services.positions import PositionsService
from .services.keywords import KeywordsService
from .services.projects import ProjectsService


class ServiceFactory:
    def __init__(self, api_client):
        self.api_client = api_client
        self._services = {}

    def get_service(self, service_name):
        """
        Возвращает экземпляр сервиса. Если сервис еще не создан, создает его.
        """
        if service_name not in self._services:
            if service_name == "positions":
                self._services[service_name] = PositionsService(self.api_client)
            elif service_name == "keywords":
                self._services[service_name] = KeywordsService(self.api_client)
            elif service_name == "projects":
                self._services[service_name] = ProjectsService(self.api_client)
            else:
                raise ValueError(f"Неизвестный сервис: {service_name}")
        return self._services[service_name]


class Topvisor:
    def __init__(self, user_id, api_key):
        self.api_client = TopvisorAPI(user_id, api_key)
        self.service_factory = ServiceFactory(self.api_client)

    def run_task(self, task_name, **kwargs):

        if task_name == "get_summary_chart":
            positions_service = self.service_factory.get_service("positions")
            return positions_service.get_summary_chart(**kwargs)
        elif task_name == "get_projects":
            projects_service = self.service_factory.get_service("projects")
            return projects_service.get_projects(**kwargs)
        elif task_name == "get_keywords_folders":
            keywords_service = self.service_factory.get_service("keywords")
            return keywords_service.get_folders(**kwargs)
        else:
            raise ValueError(f"Неизвестная задача: {task_name}")
