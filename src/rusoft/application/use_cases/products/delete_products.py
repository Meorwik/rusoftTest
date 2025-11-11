from rusoft.domain.contracts.database.repositories import ProductRepository


class DeleteProductsUseCase:
    def __init__(self, product_repo: ProductRepository):
        self._repo = product_repo

    async def __call__(self) -> bool:
        await self._repo.remove_all_products()
        is_empty: bool = await self._repo.is_empty()
        return is_empty
