from dataclasses import asdict

from src.rusoft.application.dto.products import ProductReadDTO
from src.rusoft.domain.contracts.database.repositories import ProductRepository
from src.rusoft.domain.entities.product import Product


class GetProductsUseCase:
    def __init__(self, product_repo: ProductRepository):
        self._repo = product_repo

    async def __call__(self) -> list[ProductReadDTO]:
        products: list[Product] = await self._repo.get_all_products()
        return [
            ProductReadDTO(**asdict(product))
            for product in products
        ]

