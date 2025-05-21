from ninja import Schema, Field
from products.schemas import ProductBase
from typing import Literal


class ProductListOutSchema(ProductBase):
    class ColorSchema(Schema):
        name: str
        color: str

    description: str
    colors: list[ColorSchema]

    @staticmethod
    def resolve_colors(o):
        return o.colors.values('name', 'color')


class ProductCreateInSchema(Schema):
    class ColorSchema(Schema):
        name: str
        color: str

    title: str
    price: int
    discount_percentage: int
    tags: list[str]
    thumbnail_url: str | None = None
    category_slug: str
    description: str
    colors: list[ColorSchema]


class ProductUpdateInSchema(Schema):
    class ColorSchema(Schema):
        name: str
        color: str

    title: str
    price: int
    discount_percentage: int
    tags: list[str]
    thumbnail_url: str | None = None
    category_slug: str
    description: str
    colors: list[ColorSchema]


class CategoriesListOutSchema(Schema):
    title: str
    thumbnail_url: str | None
    slug: str


class CategoryCreateInSchema(Schema):
    title: str
    thumbnail_url: str | None = None
    slug: str


class CategoryUpdateInSchema(Schema):
    title: str
    thumbnail_url: str | None = None
    slug: str


class OrderListOutSchema(Schema):
    id: int

    class OrderItem(Schema):
        id: int = Field(alias='product.id')
        title: str = Field(alias='product.title')
        thumbnail_url: str | None = Field(None, alias='product.thumbnail_url')
        quantity: int
        price: int

    items: list[OrderItem]
    full_name: str
    postal_code: str = Field(min_length=10, max_length=10)
    address: str
    payment_type: Literal['in_place', 'installment', 'online']
    status: Literal['pending', 'cancelled', 'completed']


class OrderUpdateInSchema(Schema):
    status: Literal['pending', 'cancelled', 'completed']
