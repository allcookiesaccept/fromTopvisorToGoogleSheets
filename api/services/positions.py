from .base_service import BaseService
from .payload_factory import PayloadFactory


class PositionsService(BaseService):

    def __init__(self, api_client):
        super().__init__(api_client)
        self.endpoints = {
            "history": "/v2/json/get/positions_2/history",
            "summary": "/v2/json/get/positions_2/summary",
            "summary_chart": "/v2/json/get/positions_2/summary/chart",
            "checker_price": "/v2/json/get/positions_2/checker/price",
            "searchers_regions_export": "/v2/json/get/positions_2/searchers/regions/export",
        }

    def get_history(
        self, project_id, regions_indexes, dates=None, date1=None, date2=None, **kwargs
    ):
        """
        Получает историю проверки позиций.

        :param project_id: ID проекта.
        :param regions_indexes: Индексы регионов.
        :param dates: Произвольные даты проверок.
        :param date1: Начальная дата периода.
        :param date2: Конечная дата периода.
        :param kwargs: Дополнительные параметры.
        :return: Результат запроса.
        """
        payload = PayloadFactory.positions_get_history_payload(
            project_id=project_id,
            regions_indexes=regions_indexes,
            dates=dates,
            date1=date1,
            date2=date2,
            **kwargs
        )
        return self.send_request(self.endpoints["history"], payload)

    def get_summary(self, project_id, region_index, dates, **kwargs):
        """
        Получает данные сводки по выбранному проекту за две даты.

        :param project_id: ID проекта.
        :param region_index: Индекс региона.
        :param dates: Две даты для построения сводки.
        :param kwargs: Дополнительные параметры.
        :return: Результат запроса.
        """
        payload = PayloadFactory.positions_get_summary_payload(
            project_id=project_id, region_index=region_index, dates=dates, **kwargs
        )
        return self.send_request(self.endpoints["summary"], payload)

    def get_summary_chart(
        self, project_id, region_index, dates=None, date1=None, date2=None, **kwargs
    ):
        """
        Возвращает координаты различных показателей для графика с осями: Дата/Величина показателя.

        :param project_id: ID проекта.
        :param region_index: Индекс региона.
        :param dates: Произвольные даты проверок.
        :param date1: Начальная дата периода.
        :param date2: Конечная дата периода.
        :param kwargs: Дополнительные параметры.
        :return: Результат запроса.
        """
        payload = PayloadFactory.positions_get_summary_chart_payload(
            project_id=project_id,
            region_index=region_index,
            dates=dates,
            date1=date1,
            date2=date2,
            **kwargs
        )
        return self.send_request(self.endpoints["summary_chart"], payload)

    def get_searchers_regions(self, project_id, **kwargs):
        """
        Экспортирует список регионов, добавленных в проект.

        :param project_id: ID проекта.
        :param kwargs: Дополнительные параметры.
        :return: Результат запроса.
        """
        payload = PayloadFactory.positions_get_searchers_regions_payload(
            project_id=project_id, **kwargs
        )
        return self.send_request(self.endpoints["searchers_regions_export"], payload)
