from rusoft.application.dto.products import ProductReadDTO, product_to_read_dto
from rusoft.domain.contracts.database.repositories import ProductRepository
from rusoft.domain.entities.product import Product


class GetProductsUseCase:
    def __init__(self, product_repo: ProductRepository):
        self._repo = product_repo

    async def __call__(self) -> list[ProductReadDTO]:
        products: list[Product] = await self._repo.get_all_products()
        return [product_to_read_dto(product) for product in products]

