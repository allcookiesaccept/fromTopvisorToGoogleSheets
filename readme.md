# Topvisor Data Extractor

Этот Python-скрипт извлекает данные из API Topvisor, обрабатывает их и сохраняет в локальную базу данных SQLite и Google Sheets. 

Основная цель — собрать метрики видимости и "здоровья" органического трафика из различных источников, включая Topvisor, для дальнейшего анализа в инструментах вроде Looker Studio.

---
## Особенности
- Извлекает даты истории проверок позиций и сводные данные (например, топ-позиции, средняя позиция, видимость) из API Topvisor.
- Сохраняет данные локально в SQLite с проверкой на дубликаты.
- Синхронизирует данные с Google Sheets для удобного доступа и визуализации.
- Настраивается через файлы .env и settings.yaml.
- Подробное логирование для отладки и мониторинга.
---

## Структура проекта

```
.
├── config/
│   ├── logger.py           # Настройка логгера (паттерн Singleton)
│   ├── settings.py         # Загрузчик конфигурации (env + YAML)
│   ├── .env.dist           # Шаблон переменных окружения
│   └── settings.yaml.dist  # Шаблон конфигурации проектов
├── db/
│   ├── db_interface.py     # Абстрактный интерфейс базы данных
│   ├── googlesheetwriter.py# Интеграция с API Google Sheets
│   └── sqlitedb.py         # Реализация базы данных SQLite
├── manager.py              # Основная бизнес-логика
└── README.md               # Этот файл

```
---

## Настройка

### Требования
- Python 3.8+
- Ключ API Topvisor и ID пользователя
- Учетные данные Google Sheets API (JSON-файл сервисного аккаунта)
- Необходимые пакеты: `pip install -r requirements.txt` (создайте файл с зависимостями, такими как pytopvisor, google-api-python-client, python-dotenv, pyyaml)

### Переменные окружения

Скопируйте config/.env.dist в config/.env и заполните:
```env
TOPVISOR_API="ваш-api-ключ"
USER_ID="ваш-id-пользователя"
GOOGLE_SHEETS_ID="id-вашей-таблицы"
SERVICE_FILE_NAME="файл-сервисного-аккаунта.json"
```

### Конфигурация проектов
Файл settings.yaml определяет проекты для мониторинга. Каждый проект требует:

- `project_id`: Уникальный ID проекта в Topvisor.
- `region_index`: Индекс региона для отслеживания позиций (например, 30).
- `project_name`: Описательное имя (опционально, для удобства).

Это базовые настройки, для проектов также можно передавать `folder_id`, `group_id` и ряд других параметров поддерживаемых библиотекой https://pypi.org/project/pytopvisor/

### файл сервисного аккаунта Google
Сохраните ваш `файл-сервисного-аккаунта.json` в папке `config/`.

---
## Использование
Запустите скрипт для извлечения и обработки данных по всем настроенным проектам:

```bash
python manager.py
```
- По умолчанию данные запрашиваются за последние 3 дня (days_back=3).
- Настройте период, передав days_back в ProjectManager.run(days_back=<число>).
### Результат
- SQLite: Данные сохраняются в data.db в таблице project_data.
- Google Sheets: Данные синхронизируются в указанную таблицу в "Sheet1".
---

## Обзор кода
- `manager.py`: Управляет процессом — извлекает даты, получает сводные данные, сохраняет в SQLite и синхронизирует с Google Sheets.
- `config/logger.py`: Реализует логгер (паттерн Singleton) с выводом в файл и консоль.
- `config/settings.py`: Загружает и проверяет конфигурацию из .env и settings.yaml.
- `db/sqlitedb.py`: Управляет хранением в SQLite с составным первичным ключом (date, project_id, region_index).
- `db/googlesheetwriter.py`: Обрабатывает операции чтения/записи в Google Sheets.
---
## Логирование
Логи сохраняются в logs/app.log и выводятся в консоль:
- `DEBUG`: Подробная информация о выполнении.
- `INFO`: Ключевые этапы.
- `ERROR`: Ошибки с трассировкой стека.