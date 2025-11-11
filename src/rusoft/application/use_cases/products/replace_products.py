from rusoft.application.dto.products import ProductReadDTO, product_to_read_dto
from rusoft.domain.contracts.database.repositories.products import ProductRepository
from rusoft.domain.entities.product import Product


class ReplaceProductsUseCase:
    def __init__(self, product_repo: ProductRepository):
        self._repo = product_repo

    async def __call__(self, products: list[Product]) -> list[ProductReadDTO]:
        added_products: list[Product] = await self._repo.replace_products(products)
        return [product_to_read_dto(product) for product in added_products]

