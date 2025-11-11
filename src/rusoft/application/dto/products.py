from dataclasses import dataclass
from typing import Optional

from rusoft.domain.entities.product import ProductId, ProductImage, Weights


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
    image_url: Optional[ProductImage]