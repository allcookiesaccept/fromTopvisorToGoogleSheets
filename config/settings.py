import os
import yaml
from pathlib import Path
from dotenv import load_dotenv
from typing import Any
from config.logger import logger

class EnvLoader:
    def __init__(self, env_path: Path):
        self.env_path = env_path
        self.data = {}
        self.load()

    def load(self):
        if self.env_path.exists():
            load_dotenv(self.env_path)
            self.data = {key: os.getenv(key) for key in os.environ}

class YAMLLoader:
    def __init__(self, yaml_path: Path):
        self.yaml_path = yaml_path
        self.data = {}
        self.load()

    def load(self):
        if self.yaml_path.exists():
            with open(self.yaml_path, "r", encoding="utf-8") as file:
                self.data = yaml.safe_load(file)
        else:
            self.data = {}


class Config:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
            cls._instance._load_config()
        return cls._instance

    def _load_config(self):
        logger.debug("Loading configuration...")

        BASE_DIR = Path(os.getenv("BASE_DIR", Path(__file__).resolve().parent.parent))
        env_loader = EnvLoader(BASE_DIR / "config" / ".env")
        yaml_loader = YAMLLoader(BASE_DIR / "config" / "settings.yaml")

        self._data = {
            "base_dir": str(BASE_DIR),
            "api_key": env_loader.data.get("TOPVISOR_API"),
            "user_id": env_loader.data.get("USER_ID"),
            "google_sheets": env_loader.data.get("GOOGLE_SHEETS_ID"),
            "service_file": env_loader.data.get("SERVICE_FILE_NAME"),
            "projects": yaml_loader.data.get("projects", {}),
        }
        logger.debug(f"Configuration loaded: {self._data}")
        self.validate()
        logger.info("Configuration validated successfully.")

    def validate(self):
        required_fields = ["api_key", "user_id", "projects"]
        for field in required_fields:
            if field not in self._data or not self._data[field]:
                raise ValueError(f"Missing or empty required field: {field}")

    def get(self, key, default=None):
        return self._data.get(key, default)

    @property
    def user_id(self) -> str:
        """Get the user_id."""
        return self._data["user_id"]

    @property
    def api_key(self) -> str:
        """Get the api_key."""
        return self._data["api_key"]

    @property
    def projects(self) -> dict[Any, Any]:
        """Get the list of projects."""
        return self._data["projects"]

    @property
    def google_sheets(self) -> str | None:
        """Get the Google Sheets settings."""
        return self._data["google_sheets"]

    def __getitem__(self, key):
        return self._data[key]

    def __setitem__(self, key, value):
        self._data[key] = value

    def __repr__(self):
        return f"<Config: {self._data}>"