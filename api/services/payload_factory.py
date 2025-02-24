from typing import List, Any, Optional, Dict, Callable
from functools import wraps


def add_universal_params(func: Callable) -> Callable:
    """
    Декоратор для добавления универсальных параметров в payload.
    Поддерживаемые параметры: limit, offset, fields, filters, id, orders.
    """

    @wraps(func)
    def wrapper(*args, **kwargs) -> Dict[str, Any]:
        # Вызов основного метода для получения базового payload
        payload = func(*args, **kwargs)

        # Универсальные параметры
        universal_params = {
            "limit": int,
            "offset": int,
            "fields": list,
            "filters": dict,
            "id": int,
            "orders": list,
        }

        # Добавление универсальных параметров, если они переданы
        for param, param_type in universal_params.items():
            if param in kwargs:
                value = kwargs[param]
                if not isinstance(value, param_type):
                    raise ValueError(
                        f"Параметр '{param}' должен быть типа {param_type.__name__}"
                    )
                payload[param] = value

        return payload

    return wrapper


class PayloadFactory:

    @staticmethod
    @add_universal_params
    def positions_get_history_payload(
        project_id: int,
        regions_indexes: List[int],
        dates: Optional[List[str]] = None,
        date1: Optional[str] = None,
        date2: Optional[str] = None,
        **kwargs,
    ) -> Dict[str, Any]:
        """
        Генерирует payload для метода positions_2/history

        Обязательные параметры:
        - project_id: int: ID проекта
        - regions_indexes: array(int): Список индексов регионов

        Необходимо указать либо:
        - dates: array of date: Список произвольных дат
        Или:
        - date1 и date2: date: Период проверок

        Дополнительные параметры:
        - fields: array fields: Возвращаемые поля объекта "Ключевая фраза"
        - competitors_ids: array(int): ID конкурентов (или ID проекта), добавленных в настройках проекта
        - type_range: enum(0, 1, 2, 3, 4, 5, 6, 7, 100): Период дат
        - count_dates: int: Максмальное число возвращаемых дат (не более 31)
        - only_exists_first_date: boolean: Отображать только ключевые фразы, присутствующие в первой проверке указанного периода
        - show_headers: boolean: Добавить в результат заголовки результатов
        - show_exists_dates: boolean: Добавить в результат даты, в которых были проверки
        - show_visitors: boolean: Добавить в результат данные об общем количество визитов по каждой проверке
        - show_top_by_depth: int: Добавить в результат данные по ТОПу указанной глубины по каждой проверке
        - positions_fields: array('position', 'snippet', 'relevant_url', 'visitors'): Выбор столбцов данных с результатами проверки
        - filter_by_dynamic: set('>', '<', '='): Фильтр по ключевым фразам
        - filter_by_positions: array of array(int, int): Фильтр по ключевым фразам, позиции которых входят в указанные промежутки
        """
        # Базовая структура payload
        payload: Dict[str, Any] = {
            "project_id": project_id,
            "regions_indexes": regions_indexes,
        }

        # Обработка дат
        if dates:
            payload["dates"] = dates
        elif date1 and date2:
            payload.update({"date1": date1, "date2": date2})
        else:
            raise ValueError("Необходимо указать либо 'dates', либо 'date1' и 'date2'")

        # Добавление опциональных параметров
        optional_params = [
            "fields",
            "competitors_ids",
            "type_range",
            "count_dates",
            "only_exists_first_date",
            "show_headers",
            "show_exists_dates",
            "show_visitors",
            "show_top_by_depth",
            "positions_fields",
            "filter_by_dynamic",
            "filter_by_positions",
        ]

        for param in optional_params:
            value = locals().get(param)
            if value is not None:
                payload[param] = value

        return payload

    @staticmethod
    @add_universal_params
    def positions_get_summary_payload(
        project_id: int,
        regions_indexes: List[int],
        dates: Optional[List[str]] = None,
        **kwargs,
    ) -> Dict[str, Any]:
        """
        https://topvisor.com/ru/api/positions-2/get-summary/

        Обязательные параметры:
        - project_id: int: ID проекта
        - regions_indexes: int: Список индексов регионов
        - dates: array(date, date): Список произвольных дат

        Дополнительные параметры:
        - competitor_id: int:ID конкурента, добавленного в настройках проекта.
        - only_exists_first_date: boolean: Учитывать ключевые фразы, присутствующие в обеих датах
        - show_dynamics: boolean: Добавить в результат динамику позиций (рост/падение)
        - show_tops: boolean: Добавить в результат данные по ТОПам
        - show_avg: boolean: Добавить в результат среднюю позицию
        - show_visibility: boolean: Добавить в результат видимость
        - show_median: boolean: Добавить в результат медианную

        :return: payload для метода get/positions_2/summary
        """

        # Базовая структура payload
        payload: Dict[str, Any] = {
            "project_id": project_id,
            "regions_indexes": regions_indexes,
            "dates": dates,
        }

        # Добавление опциональных параметров
        optional_params = [
            "competitor_id",
            "only_exists_first_date",
            "show_dynamics",
            "show_tops",
            "show_avg",
            "show_visibility",
            "show_median",
        ]

        for param in optional_params:
            value = locals().get(param)
            if value is not None:
                payload[param] = value

        return payload

    @staticmethod
    @add_universal_params
    def positions_get_summary_chart_payload(
        project_id: int,
        regions_indexes: List[int],
        dates: Optional[List[str]] = None,
        date1: Optional[str] = None,
        date2: Optional[str] = None,
        **kwargs,
    ) -> Dict[str, Any]:
        """
        https://topvisor.com/ru/api/positions-2/get-summary-chart/

        Обязательные параметры:

        :param project_id: int: ID проекта.
        :param regions_indexes: int: Список индексов регионов.
        :param dates: array of date: Произвольные даты проверок.
        :param date1: date: Начальная дата периода проверок.
        :param date2: date: Конечная дата периода проверок.

        Дополнительные параметры:
        :param competitors_ids: array: ID конкурентов (или ID проекта), добавленных в настройках проекта.
        :param type_range: array: Период дат (опционально).
        :param only_exists_first_date: boolean: Учитывать ключевые фразы, присутствующие во всех датах
        :param show_tops: boolean: Добавить в результат данные по ТОПам
        :param show_avg: boolean: Добавить в результат среднюю позицию
        :param show_visibility: boolean: Добавить в результат видимость

        :return: payload для метода get/positions_2/summary/chart
        """
        # Базовая структура payload
        payload: Dict[str, Any] = {
            "project_id": project_id,
            "regions_indexes": regions_indexes,
        }

        # Обработка дат
        if dates:
            payload["dates"] = dates
        elif date1 and date2:
            payload.update({"date1": date1, "date2": date2})
        else:
            raise ValueError("Необходимо указать либо 'dates', либо 'date1' и 'date2'")

        # Добавление опциональных параметров
        optional_params = [
            "competitors_ids",
            "type_range",
            "only_exists_first_date",
            "show_tops",
            "show_avg",
            "show_visibility",
        ]

        for param in optional_params:
            value = locals().get(param)
            if value is not None:
                payload[param] = value

        return payload

    @staticmethod
    @add_universal_params
    def positions_get_searchers_regions_payload(
        project_id: int, **kwargs
    ) -> Dict[str, Any]:
        """
        https://topvisor.com/ru/api/positions-2/get-searchers-regions-export/

        Обязательные параметры:

        :param project_id: int: ID проекта.

        Дополнительные параметры: # https://topvisor.com/ru/api/positions-2/add-searchers/
        :param searcher_key: int: Ключ поисковой системы
        :param name/key: int: Название/ключ региона
        :param country_code: string: Двухбуквенный код страны
        :param lang: string: Язык интерфейса
        :param device: enum(0, 1, 2): Тип устройства
        :param depth: int: Глубина проверки

        :return: payload для метода get/positions_2/searchers/regions/export

        """
        # Базовая структура payload
        payload: Dict[str, Any] = {
            "project_id": project_id,
        }

        # Добавление опциональных параметров
        optional_params = [
            "searcher_key",
            "name/key",
            "country_code",
            "lang",
            "device",
            "depth",
        ]

        for param in optional_params:
            value = locals().get(param)
            if value is not None:
                payload[param] = value

        return payload
