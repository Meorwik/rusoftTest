from dataclasses import asdict

from src.rusoft.application.dto.products import ProductReadDTO
from src.rusoft.domain.contracts.database.repositories.products import ProductRepository
from src.rusoft.domain.entities.product import Product


class ReplaceProductsUseCase:
    def __init__(self, product_repo: ProductRepository):
        self._repo = product_repo

    async def __call__(self, products: list[Product]) -> list[ProductReadDTO]:
        added_products: list[Product] = await self._repo.replace_products(products)
        return [
            ProductReadDTO(**asdict(product))
            for product in added_products
        ]

