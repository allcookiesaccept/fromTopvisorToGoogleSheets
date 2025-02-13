import os
import yaml
from pathlib import Path
from dotenv import load_dotenv


class Config:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
            cls._instance._load_config()
        return cls._instance

    def _load_config(self):
        self.BASE_DIR = Path(__file__).resolve().parent.parent

        env_path = self.BASE_DIR / "config" / ".env"
        if env_path.exists():
            load_dotenv(env_path)

        yaml_path = self.BASE_DIR / "config" / "settings.yaml"
        if yaml_path.exists():
            with open(yaml_path, "r", encoding="utf-8") as file:
                self.yaml_data = yaml.safe_load(file)
        else:
            self.yaml_data = {}

        self.data = {
            "BASE_DIR": str(self.BASE_DIR),
            "API_BASE_URL": self.yaml_data.get("api", {}).get("base_url"),
            "DEFAULT_METRICS": self.yaml_data.get("api", {}).get("default_metrics"),
            "DEFAULT_TOPS": self.yaml_data.get("api", {}).get("default_tops"),
            "GOOGLE_SHEETS": {
                "workbook_id": os.getenv("GOOGLE_SHEETS_WORKBOOK_ID"),
                "service_file_path": os.getenv("GOOGLE_SERVICE_ACCOUNT_PATH"),
            },
            "TOPVISOR_API": os.getenv("TOPVISOR_API_KEY"),
            "USER_ID": os.getenv("USER_ID"),
            "PROJECTS": self.yaml_data.get("projects", {}),
        }

    def get_project(self, project_name):
        projects = self.data.get("PROJECTS", {})
        return projects.get(project_name)

    def list_projects(self):
        return list(self.data.get("PROJECTS", {}).keys())

    def get_default_metrics(self):
        return self.data.get("DEFAULT_METRICS", [])

    def get_default_tops(self):
        return self.data.get("DEFAULT_TOPS", [])

    def get(self, key, default=None):
        return self.data.get(key, default)

    def __getitem__(self, key):
        return self.data[key]

    def __setitem__(self, key, value):
        self.data[key] = value

    def __repr__(self):
        return f"<Config: {self.data}>"
