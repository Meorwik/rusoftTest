from dataclasses import dataclass


@dataclass
class DatabaseConfig:
    host: str
    port: int
    password: str
    user: str
    database: str

    @property
    def address(self) -> str:
        return f"{self.host}:{self.port}"

    @property
    def sqlalchemy_uri(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"