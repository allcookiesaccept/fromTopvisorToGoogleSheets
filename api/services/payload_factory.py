class PayloadFactory:
    @staticmethod
    def generate_summary_chart_payload(
        project_id,
        region_index,
        dates,
        show_visibility=True,
        show_avg=True,
        show_tops=True,
    ):
        """
        Генерирует payload для метода summary/chart.
        """
        return {
            "project_id": project_id,
            "region_index": region_index,
            "dates": dates,
            "show_visibility": show_visibility,
            "show_avg": show_avg,
            "show_tops": show_tops,
        }

    @staticmethod
    def generate_keywords_payload(project_id, view="tree", show_trash=False):
        """
        Генерирует payload для метода keywords/folders.
        """
        return {"project_id": project_id, "view": view, "show_trash": show_trash}
