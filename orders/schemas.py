from typing import Literal

from ninja import Schema, Field


class OrderCreateInSchema(Schema):
    full_name: str
    postal_code: str = Field(min_length=10, max_length=10)
    address: str
    payment_type: Literal['in_place', 'installment', 'online']


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
