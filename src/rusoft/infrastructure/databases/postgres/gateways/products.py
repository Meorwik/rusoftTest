from sqlalchemy import delete, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from rusoft.domain.contracts.database import ProductRepository
from rusoft.domain.entities import Product, ProductId, ProductImage
from rusoft.infrastructure.databases.postgres.models import ProductModel


class ProductsGateway(ProductRepository):

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def add_products(self, products: list[Product]) -> list[Product]:
        result_products = []
        for product in products:
            stmt = insert(ProductModel).values(
                uid_product=product.uid_product,
                name=product.name,
                description=product.description,
                short_description=product.short_description,
                uid_groups=product.uid_groups,
                features=product.features,
                uid_features=product.uid_features,
                hash=product.hash,
                is_weighted=product.is_weighted,
                image_url=product.image_url,
            ).on_conflict_do_update(
                index_elements=["uid_product"],
                set_={
                    "name": product.name,
                    "description": product.description,
                    "short_description": product.short_description,
                    "uid_groups": product.uid_groups,
                    "features": product.features,
                    "uid_features": product.uid_features,
                    "hash": product.hash,
                    "is_weighted": product.is_weighted,
                    "image_url": product.image_url,
                },
            )
            await self._session.execute(stmt)
            result_products.append(product)

        await self._session.commit()
        return result_products


    async def replace_products(self, products: list[Product]) -> list[Product]:
        await self.remove_all_products()
        return await self.add_products(products)

    async def add_image(self, product_id: ProductId, image: ProductImage) -> Product:
        query = select(ProductModel).where(product_id == ProductModel.uid_product)
        result = await self._session.execute(query)
        product: ProductModel | None = result.scalar_one_or_none()

        if not product:
            raise ValueError(f"Product {product_id} not found")

        product.image_url = image.url
        await self._session.commit()
        await self._session.refresh(product)

        return Product.from_orm(product)

    async def is_empty(self) -> bool:
        result = await self._session.execute(select(ProductModel).limit(1))
        return result.scalar_one_or_none() is None

    async def remove_all_products(self) -> bool:
        await self._session.execute(delete(ProductModel))
        await self._session.commit()
        return await self.is_empty()

    async def get_all_products(self) -> list[Product]:
        result = await self._session.execute(select(ProductModel))
        rows = result.scalars().all()
        return [Product.from_orm(row) for row in rows]