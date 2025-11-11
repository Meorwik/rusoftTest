from rusoft.application.dto.products import ProductReadDTO, product_to_read_dto
from rusoft.domain.contracts.database.repositories import ProductRepository
from rusoft.domain.entities.product import Product


class AddProductsUseCase:

    def __init__(self, products_repo: ProductRepository) -> None:
        self._repo = products_repo

    async def __call__(self, products: list[Product]) -> list[ProductReadDTO]:
        full_product_list: list[Product] = await self._repo.add_products(products)
        return [product_to_read_dto(product) for product in full_product_list]