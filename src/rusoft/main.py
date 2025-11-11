from pathlib import Path
from typing import Final

from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI

from rusoft.application.container import get_container
from rusoft.config.provider import DatabaseConfigProvider
from rusoft.presentation import api_router

database_config_provider = DatabaseConfigProvider(path=Path("properties.yaml"), section="postgres")

app: Final[FastAPI] = FastAPI()
app.include_router(api_router, prefix="/api")

setup_dishka(get_container(database_config_provider), app)

