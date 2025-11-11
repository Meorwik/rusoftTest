from dataclasses import dataclass, field
from typing import NewType, Optional
from uuid import UUID, uuid4

from .enums import Weights

ProductId = NewType("ProductId", UUID)

@dataclass
class ProductImage:
    url: str


@dataclass(frozen=True)
class Product:
    name: str
    uid_product: ProductId = field(default_factory=uuid4)
    description: Optional[str] = None
    short_description: Optional[str] = None
    uid_groups: Optional[str] = None
    features: Optional[str] = None
    uid_features: Optional[str] = None
    hash: Optional[str] = None
    is_weighted: bool = False
    weight_type: Optional[Weights] = None
    image: Optional[ProductImage] = None

    @property
    def image_url(self) -> Optional[str]:
        return self.image.url if self.image else None