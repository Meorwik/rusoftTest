from dataclasses import asdict
from uuid import UUID

from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, File, UploadFile
from starlette.responses import JSONResponse

from rusoft.application.use_cases.products import (
    AddImageUseCase,
    AddProductsUseCase,
    DeleteProductsUseCase,
    GetProductsUseCase,
    ReplaceProductsUseCase,
)
from rusoft.presentation.schemas import ProductListIn, ProductListOut, ProductRead

products_router = APIRouter()


@products_router.post("/add")
@inject
async def add_products(use_case: FromDishka[AddProductsUseCase], products: ProductListIn) -> ProductListOut:
    print(use_case)


@products_router.post("/replace")
@inject
async def replace_products(use_case: FromDishka[ReplaceProductsUseCase], products: ProductListIn) -> ProductListOut:
    ...


@products_router.delete("/")
@inject
async def delete_products(use_case: FromDishka[DeleteProductsUseCase]) -> JSONResponse:
    ...


@products_router.post("/{uid_product}/upload-image")
@inject #use_case: FromDishka[AddImageUseCase]
async def upload_image(uid_product: UUID, image: UploadFile = File(...)) -> ProductRead:
    print(1123)
    return ProductRead()


@products_router.get("/")
@inject
async def get_products(use_case: FromDishka[GetProductsUseCase]) -> ProductListOut:
    ...