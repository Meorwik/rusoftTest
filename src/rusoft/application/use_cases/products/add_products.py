from dataclasses import asdict

from src.rusoft.application.dto.products import ProductReadDTO
from src.rusoft.domain.contracts.database.repositories import ProductRepository
from src.rusoft.domain.entities.product import Product


class AddProductsUseCase:

    def __init__(self, products_repo: ProductRepository) -> None:
        self._repo = products_repo

    async def __call__(self, products: list[Product]) -> list[ProductReadDTO]:
        full_product_list: list[Product] = await self._repo.add_products(products)
        return [
            ProductReadDTO(**asdict(product))
            for product in full_product_list
        ]