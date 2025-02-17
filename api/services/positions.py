from .base_service import BaseService
from .payload_factory import PayloadFactory


class PositionsService(BaseService):

    def __init__(self, api_client):
        super().__init__(api_client)
        self.summary_endpoint = "/v2/json/get/positions_2/summary_chart"

    def get_summary_chart(self, project_id, region_index, dates, **kwargs):

        payload = PayloadFactory.generate_positions_summary_chart_payload(
            project_id=project_id, region_index=region_index, dates=dates, **kwargs
        )
        return self.send_request(self.summary_endpoint, payload)
