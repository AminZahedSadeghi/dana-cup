from ninja import Schema, Field


class ProductBase(Schema):
    id: int
    title: str
    slug: str
    price: int
    discount_price: int
    discount_percentage: int
    is_discount: bool
    tags: list[str]
    thumbnail_url: str | None
    category: str | None = Field(None, alias='category.title')

    @staticmethod
    def resolve_tags(o):
        return list(o.tags.values_list('name', flat=True)) if o.tags.count() != 0 else []


class ProductListOutSchema(ProductBase):
    pass


class ProductDetailOutSchema(ProductBase):
    class ColorSchema(Schema):
        name: str
        color: str

    description: str
    colors: list[ColorSchema]

    @staticmethod
    def resolve_colors(o):
        return o.colors.values('name', 'color')


class CategoryListOutSchema(Schema):
    title: str
    thumbnail_url: str | None
    slug: str


class CategoryProductListOutSchema(Schema):
    title: str
    slug: str
    price: int
    discount_price: int
    discount_percentage: int
    is_discount: bool
    tags: list[str]
    thumbnail_url: str | None
    category: str | None = Field(None, alias='category.title')

    @staticmethod
    def resolve_tags(o):
        return list(o.tags.values_list('name', flat=True)) if o.tags.count() != 0 else []
