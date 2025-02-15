from .base_service import BaseService
from .payload_factory import PayloadFactory


class PositionsService(BaseService):
    def get_summary_chart(self, project_id, region_index, dates, **kwargs):
        """
        Получает данные сводки позиций.
        """
        payload = PayloadFactory.generate_summary_chart_payload(
            project_id=project_id, region_index=region_index, dates=dates, **kwargs
        )
        endpoint = "/v2/json/get/positions_2/summary_chart"
        return self.send_request(endpoint, payload)
