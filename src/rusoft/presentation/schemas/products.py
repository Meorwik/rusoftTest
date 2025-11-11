from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field

from rusoft.presentation.schemas.enums import Weights


class ProductBase(BaseModel):
    uid_product: UUID = Field(...)
    name: str
    description: Optional[str] = None
    short_description: Optional[str] = None
    uid_groups: Optional[str] = None
    features: Optional[str] = None
    uid_features: Optional[str] = None
    hash: Optional[str] = None
    is_weighted: bool | Weights = Field(default=False)
    image_url: Optional[str] = Field(default=None)


class ProductCreate(ProductBase):
    ...


class ProductListIn(BaseModel):
    products: list[ProductCreate]


class ProductRead(ProductBase):
    ...


class ProductListOut(BaseModel):
    products: list[ProductRead]
