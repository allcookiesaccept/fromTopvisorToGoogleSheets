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

    def get_operation_mapping(self):
        """
        Возвращает словарь маппинга операций.
        Ключ: имя операции.
        Значение: кортеж (сервис, метод).
        """
        return {
            "get_summary_chart": ("positions", "get_summary_chart"),
            "get_projects": ("projects", "get_projects"),
            "get_keywords_folders": ("keywords", "get_folders"),
            "get_competitors": ("projects", "get_competitors"),
            "get_regions_and_searchers": ("projects", "get_regions_and_searchers"),
            "get_keywords_groups": ("keywords", "get_groups"),
            "get_keywords_volume": ("keywords", "get_volume"),
        }

    def run_task(self, task_name, **kwargs):
        """
        Универсальный метод для выполнения операций.

        :param operation_name: Название операции.
        :param kwargs: Аргументы для операции.
        :return: Результат выполнения операции.
        """

        operation_mapping = self.get_operation_mapping()

        if task_name not in operation_mapping:
            raise ValueError(f"Unknown operation: {task_name}")

        service_name, method_name = operation_mapping[task_name]
        service = self.service_factory.get_service(service_name)

        method = getattr(service, method_name, None)

        if not method:
            raise AttributeError(
                f"Метод {method_name} не найден в сервисе {service_name}"
            )

        return method(**kwargs)
