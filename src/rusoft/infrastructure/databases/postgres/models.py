import uuid

from sqlalchemy import (
    Boolean,
    Enum,
    String,
    text,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from rusoft.infrastructure.databases.postgres.enums import Weights

from .base import Base


class ProductModel(Base):
    __tablename__ = "products"

    uid_product: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        server_default=text("gen_random_uuid()"),
    )

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(String(1000), nullable=False)
    short_description: Mapped[str] = mapped_column(String(500), nullable=True)

    uid_groups: Mapped[str] = mapped_column(String(255), nullable=True)
    features: Mapped[str] = mapped_column(String(500), nullable=True)
    uid_features: Mapped[str] = mapped_column(String(255), nullable=True)

    hash: Mapped[str] = mapped_column(String(255), nullable=True)
    is_weighted: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    weight: Mapped[Weights] = mapped_column(Enum(Weights), nullable=True)

    image_url: Mapped[str | None] = mapped_column(String(500), nullable=True)