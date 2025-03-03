import os
import logging
from pathlib import Path


class Logger:
    _instance = None

    def __new__(cls, log_file="app.log"):
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
            cls._instance._setup_logger(log_file)
        return cls._instance

    def _setup_logger(self, log_file):
        """
        Настройка логгера.
        """
        self.logger = logging.getLogger("TopvisorLogger")
        self.logger.setLevel(logging.DEBUG)

        # Проверяем, есть ли уже обработчики
        if not self.logger.handlers:
            # Создание директории для логов, если её нет
            logs_dir = Path(__file__).resolve().parent.parent / "logs"
            logs_dir.mkdir(exist_ok=True)

            # Формат логов
            formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

            # Логирование в файл
            file_handler = logging.FileHandler(logs_dir / log_file, encoding="utf-8")
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(formatter)

            # Логирование в консоль
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.INFO)
            console_handler.setFormatter(formatter)

            # Добавление обработчиков
            self.logger.addHandler(file_handler)
            self.logger.addHandler(console_handler)

    def get_logger(self):
        """
        Возвращает экземпляр логгера.
        """
        return self.logger


# Глобальный экземпляр логгера
logger = Logger().get_logger()


def debug(func):
    """
    Декоратор для логирования выполнения функции.
    """

    def wrapper(*args, **kwargs):
        logger = Logger().get_logger()
        func_name = func.__name__
        logger.debug(f"Выполнение функции '{func_name}' начато.")
        try:
            result = func(*args, **kwargs)
            logger.debug(f"Функция '{func_name}' успешно завершена.")
            return result
        except Exception as e:
            logger.error(f"Ошибка в функции '{func_name}': {e}")
            raise

    return wrapper
