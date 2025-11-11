
from typing import AsyncIterable

from dishka import AnyOf, Provider, Scope, from_context, provide
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from rusoft.config.provider import DatabaseConfigProvider
from rusoft.domain.contracts.database import (
    ProductRepository,
)
from rusoft.infrastructure.databases.postgres import (
    ProductsGateway,
    new_session_maker,
)


class ProductsGateProvider(Provider):
    products_gate = provide(
        ProductsGateway,
        provides=AnyOf[ProductRepository],
        scope=Scope.REQUEST,
    )


class SessionProvider(Provider):
    config = from_context(provides=DatabaseConfigProvider, scope=Scope.APP)

    @provide(scope=Scope.APP)
    def get_session_maker(self, config_provider: DatabaseConfigProvider) -> async_sessionmaker[AsyncSession]:
        session_maker: async_sessionmaker[AsyncSession] = new_session_maker(config_provider.config)
        return session_maker

    @provide(scope=Scope.REQUEST)
    async def get_session(self, session_maker: async_sessionmaker[AsyncSession]) -> AsyncIterable[AsyncSession]:
        async with session_maker() as session:
            yield session
