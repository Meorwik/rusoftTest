from pathlib import Path
from typing import Iterable, List
from uuid import UUID

from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, File, HTTPException, UploadFile, status
from starlette.responses import JSONResponse

from rusoft.application.dto.products import ProductReadDTO
from rusoft.application.use_cases.products import (
    AddImageUseCase,
    AddProductsUseCase,
    DeleteProductsUseCase,
    GetProductsUseCase,
    ReplaceProductsUseCase,
)
from rusoft.domain.entities.product import Product, ProductId, ProductImage
from rusoft.presentation.schemas import ProductListIn, ProductListOut, ProductRead
from rusoft.presentation.schemas.enums import Weights
from rusoft.presentation.schemas.products import ProductCreate

products_router = APIRouter()

_UPLOAD_DIR = Path("build/uploads")


@products_router.post("/add", response_model=ProductListOut, status_code=status.HTTP_201_CREATED)
@inject
async def add_products(
    use_case: FromDishka[AddProductsUseCase],
    products: ProductListIn,
) -> ProductListOut:
    domain_products = _map_products_to_domain(products.products)
    result = await use_case(domain_products)
    return ProductListOut(products=_map_dtos_to_schema(result))


@products_router.post("/replace", response_model=ProductListOut)
@inject
async def replace_products(
    use_case: FromDishka[ReplaceProductsUseCase],
    products: ProductListIn,
) -> ProductListOut:
    domain_products = _map_products_to_domain(products.products)
    result = await use_case(domain_products)
    return ProductListOut(products=_map_dtos_to_schema(result))


@products_router.delete("/", status_code=status.HTTP_200_OK)
@inject
async def delete_products(use_case: FromDishka[DeleteProductsUseCase]) -> JSONResponse:
    is_empty = await use_case()
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"success": is_empty},
    )


@products_router.post("/{uid_product}/upload-image", response_model=ProductRead)
@inject
async def upload_image(
    use_case: FromDishka[AddImageUseCase],
    uid_product: UUID,
    image: UploadFile = File(...),
) -> ProductRead:
    if not image.filename:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="File name is required")

    file_bytes = await image.read()
    await image.close()
    if not file_bytes:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Uploaded file is empty")

    file_path = _save_upload(uid_product, image.filename, file_bytes)
    updated_product = await use_case(uid_product, file_path)
    return _map_dto_to_schema(updated_product)


@products_router.get("/", response_model=ProductListOut)
@inject
async def get_products(use_case: FromDishka[GetProductsUseCase]) -> ProductListOut:
    products = await use_case()
    return ProductListOut(products=_map_dtos_to_schema(products))


def _map_products_to_domain(products: Iterable[ProductCreate]) -> List[Product]:
    domain_products: List[Product] = []
    for product in products:
        is_weighted, weight_type = _decode_weight(product.is_weighted, product.weight_type)
        domain_products.append(
            Product(
                uid_product=ProductId(product.uid_product),
                name=product.name,
                description=product.description,
                short_description=product.short_description,
                uid_groups=product.uid_groups,
                features=product.features,
                uid_features=product.uid_features,
                hash=product.hash,
                is_weighted=is_weighted,
                weight_type=weight_type,
                image=ProductImage(product.image_url) if product.image_url else None,
            )
        )
    return domain_products


def _map_dtos_to_schema(dtos: Iterable[ProductReadDTO]) -> List[ProductRead]:
    return [_map_dto_to_schema(dto) for dto in dtos]


def _map_dto_to_schema(dto: ProductReadDTO) -> ProductRead:
    return ProductRead(
        uid_product=UUID(str(dto.uid_product)),
        name=dto.name,
        description=dto.description,
        short_description=dto.short_description,
        uid_groups=dto.uid_groups,
        features=dto.features,
        uid_features=dto.uid_features,
        hash=dto.hash,
        is_weighted=dto.is_weighted,
        weight_type=dto.weight_type,
        image_url=dto.image_url,
    )


def _save_upload(product_id: UUID, filename: str, content: bytes) -> str:
    _UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    safe_name = filename.replace("/", "_").replace("\\", "_")
    target_path = _UPLOAD_DIR / f"{product_id}_{safe_name}"
    target_path.write_bytes(content)
    return str(target_path)


def _decode_weight(is_weighted_value: bool | Weights, weight_type: Weights | None) -> tuple[bool, Weights | None]:
    if isinstance(is_weighted_value, Weights):
        return True, is_weighted_value
    if weight_type:
        return True, weight_type
    return bool(is_weighted_value), None