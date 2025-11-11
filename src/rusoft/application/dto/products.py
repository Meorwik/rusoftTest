from dataclasses import dataclass
from typing import Optional

from rusoft.domain.entities.product import Product, ProductId, Weights


@dataclass
class ProductReadDTO:
    uid_product: ProductId
    name: str
    description: Optional[str]
    short_description: Optional[str]
    uid_groups: Optional[str]
    features: Optional[str]
    uid_features: Optional[str]
    hash: Optional[str]
    is_weighted: bool
    weight_type: Optional[Weights]
    image_url: Optional[str]


def product_to_read_dto(product: Product) -> ProductReadDTO:
    return ProductReadDTO(
        uid_product=product.uid_product,
        name=product.name,
        description=product.description,
        short_description=product.short_description,
        uid_groups=product.uid_groups,
        features=product.features,
        uid_features=product.uid_features,
        hash=product.hash,
        is_weighted=product.is_weighted,
        weight_type=product.weight_type,
        image_url=product.image_url,
    )