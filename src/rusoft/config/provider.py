from pathlib import Path

from yaml import safe_load

from .schema import DatabaseConfig


class DatabaseConfigProvider:
    def __init__(self, path: Path, section: str = "database") -> None:
        self._path = path
        self._section = section
        self._data: dict[str, dict[str, str]] = {}

    def _load_config(self) -> None:
        with open(self._path, "r", encoding="utf-8") as file:
            data = safe_load(file)

        self._data = data

    def _validate_fields(self) -> None:
        database_section = self._data.get(self._section)
        if not database_section:
            raise ValueError(f"Missing '{self._section}' section in YAML config")

        required_fields = ["host", "port", "user", "password", "database"]
        missing = [key for key in required_fields if key not in database_section]
        if missing:
            raise ValueError(
                f"Missing required DB fields: {', '.join(missing)}"
            )

    @property
    def config(self) -> DatabaseConfig:
        self._load_config()
        self._validate_fields()

        database_data = self._data[self._section]

        return DatabaseConfig(
            host=database_data["host"],
            port=int(database_data["port"]),
            user=database_data["user"],
            password=database_data["password"],
            database=database_data["database"],
        )
