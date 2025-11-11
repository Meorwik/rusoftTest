
from typing import AsyncIterable

from dishka import AnyOf, Provider, Scope, from_context, provide
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from ...config.provider import DatabaseConfigProvider
from ...domain.contracts.database import ProductRepository
from ...infrastructure.databases.postgres import ProductsGateway, new_session_maker


class ProductsGateProvider(Provider):
    @provide(provides=AnyOf[ProductRepository], scope=Scope.REQUEST)
    def get_products_gateway(self, session: AsyncSession) -> ProductsGateway:
        return ProductsGateway(session)


class SessionProvider(Provider):
    config_provider = from_context(provides=DatabaseConfigProvider, scope=Scope.APP)

    @provide(scope=Scope.APP)
    def get_session_maker(self, config_provider: DatabaseConfigProvider) -> async_sessionmaker[AsyncSession]:
        session_maker: async_sessionmaker[AsyncSession] = new_session_maker(config_provider.config)
        return session_maker

    @provide(scope=Scope.REQUEST)
    async def get_session(self, session_maker: async_sessionmaker[AsyncSession]) -> AsyncIterable[AsyncSession]:
        async with session_maker() as session:
            yield session
