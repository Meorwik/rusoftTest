from dishka import AsyncContainer, make_async_container

from src.rusoft.config import DatabaseConfigProvider

from .providers import (
    ProductsGateProvider,
    ProductsUseCasesProvider,
    SessionProvider,
)


def get_container(config_provider: DatabaseConfigProvider) -> AsyncContainer:
    container = make_async_container(
        ProductsGateProvider(),
        ProductsUseCasesProvider(),
        SessionProvider(),
        context={DatabaseConfigProvider: config_provider},
    )
    return container