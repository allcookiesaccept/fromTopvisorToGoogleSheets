class PayloadFactory:

    @staticmethod
    def generate_positions_summary_chart_payload(
        project_id,
        region_index,
        dates,
        show_visibility=True,
        show_avg=True,
        show_tops=True,
    ):

        return {
            "project_id": project_id,
            "region_index": region_index,
            "dates": dates,
            "show_visibility": show_visibility,
            "show_avg": show_avg,
            "show_tops": show_tops,
        }

    @staticmethod
    def generate_keywords_get_folders_payload(
        project_id, view="tree", show_trash=False
    ):

        return {
            "project_id": project_id,
            "view": view,
            "show_trash": show_trash,
        }

    @staticmethod
    def generate_keywords_get_groups_payload(
        project_id, folder_id=None, show_trash=False
    ):
        """
        Получает список групп ключевых фраз.
        :param project_id: ID проекта.
        :param folder_id: ID папки (необязательно).
        :param show_trash: Показывать удаленные группы.
        :return: Список групп.
        """
        return {
            "project_id": project_id,
            "folder_id": folder_id,
            "show_trash": show_trash,
        }

    @staticmethod
    def generate_keywords_get_volume_payload(
        project_id, qualifiers, target_type="groups", filters=None
    ):
        """
        Формирует payload для запроса частоты запросов.
        :param project_id: ID проекта.
        :param qualifiers: Определители частоты (region_key, searcher_key, type).
        :param target_type: Тип объекта фильтрации (keywords или groups).
        :param filters: Фильтры для запроса.
        :return: Payload для API.
        """
        return {
            "project_id": project_id,
            "qualifiers": qualifiers,
            "target_type": target_type,
            "filters": filters or [],
        }
