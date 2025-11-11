from dataclasses import asdict
from uuid import UUID

from rusoft.application.dto.products import ProductReadDTO
from rusoft.domain.contracts.database.repositories import ProductRepository
from rusoft.domain.entities.product import Product, ProductId, ProductImage


class AddImageUseCase:
    def __init__(self, product_repo: ProductRepository):
        self._repo = product_repo

    async def __call__(self, product_uid: UUID, image) -> ProductReadDTO:
        updated_product: Product = await self._repo.add_image(ProductId(product_uid), ProductImage(image))
        return ProductReadDTO(**asdict(updated_product))