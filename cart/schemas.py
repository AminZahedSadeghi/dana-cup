from ninja import Schema, Field
from products.schemas import ProductListOutSchema


class CartAddItemInSchema(Schema):
    product_id: int = Field(gt=0)
    quantity: int = Field(gt=0)


class CartItemListOutSchema(Schema):
    id: int
    total_price: int
    quantity: int
    product: ProductListOutSchema


class CartInfoSchema(Schema):
    total_price: int
    items_count: int
    items_unique_count: int
    is_empty: bool


class CartItemUpdateInSchema(Schema):
    quantity: int = Field(gt=0)
