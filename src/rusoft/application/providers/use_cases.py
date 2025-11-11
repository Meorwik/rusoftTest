from dishka import Provider, Scope, provide

from rusoft.application.use_cases.products import (
    AddImageUseCase,
    AddProductsUseCase,
    DeleteProductsUseCase,
    GetProductsUseCase,
    ReplaceProductsUseCase,
)
from rusoft.domain.contracts.database import (
    ProductRepository,
)


class ProductsUseCasesProvider(Provider):

    @provide(scope=Scope.REQUEST)
    async def get_products(self, repo: ProductRepository) -> GetProductsUseCase:
        return GetProductsUseCase(repo)

    @provide(scope=Scope.REQUEST)
    async def add_products(self, repo: ProductRepository) -> AddProductsUseCase:
        return AddProductsUseCase(repo)

    @provide(scope=Scope.REQUEST)
    async def delete_products(self, repo: ProductRepository) -> DeleteProductsUseCase:
        return DeleteProductsUseCase(repo)

    @provide(scope=Scope.REQUEST)
    async def add_image(self, repo: ProductRepository) -> AddImageUseCase:
        return AddImageUseCase(repo)

    @provide(scope=Scope.REQUEST)
    async def replace_products(self, repo: ProductRepository) -> ReplaceProductsUseCase:
        return ReplaceProductsUseCase(repo)