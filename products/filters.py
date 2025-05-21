# price range - title - is_discount - tags<optional> - category__title
# newest - oldest - high_price - low_price - most_discount<optional>
from ninja import FilterSchema, Field
from typing import Literal
from django.db.models import Q


class ProductFilterSchema(FilterSchema):
    title: str | None = Field(None, q='title__icontains')
    category_title: str | None = Field(None, q='category__title__icontains')
    min_price: int | None = Field(None, q='discount_price__gte')
    max_price: int | None = Field(None, q='discount_price__lte')
    is_discount: bool | None = Field(None, q='is_discount')
