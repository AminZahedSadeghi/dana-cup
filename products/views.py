from typing import Literal

from django.db.models import QuerySet
from ninja import Query
from ninja.errors import HttpError
from ninja.pagination import paginate
from ninja_extra import api_controller, ControllerBase, route

from core.types import UnicodeSlugType
from .filters import ProductFilterSchema
from .models import Category, Product
from .schemas import ProductListOutSchema, ProductDetailOutSchema, CategoryListOutSchema, CategoryProductListOutSchema
from .service import ProductService


@api_controller('/products', tags=['Products'], auth=None)
class ProductController(ControllerBase):
    service = ProductService()

    @route.get('', response=list[ProductListOutSchema], url_name='products@list', description='Get product list')
    @paginate
    def product_list(
            self, ordering: Query[Literal['amazing', 'newest', 'oldest', 'high_price', 'low_price']] = 'newest',
            filters: ProductFilterSchema = Query(...),
    ):
        qs: QuerySet[Product] = filters.filter(self.service.product_list())
        match ordering:
            case 'amazing':
                qs = qs.order_by('-discount_percentage')
            case 'newest':
                qs = qs.order_by('-created_at')
            case 'oldest':
                qs = qs.order_by('created_at')
            case 'high_price':
                qs = qs.order_by('-discount_price')
            case 'low_price':
                qs = qs.order_by('discount_price')

        return qs

    @route.get('/{pk}', response=ProductDetailOutSchema, url_name='products@detail', description='Get product detail')
    def product_detail(self, pk: int):
        return self.service.product_detail(pk=pk)


@api_controller('/categories', tags=['Categories'], auth=None)
class CategoryController(ControllerBase):

    @route.get('', response=list[CategoryListOutSchema], url_name='categories@list', description='Get category list')
    def category_list(self):
        return Category.objects.all()

    @route.get('/{slug}', response=list[CategoryProductListOutSchema], url_name='categories@product_list',
               description='Get products of a category')
    def category_products(self, slug: UnicodeSlugType):
        try:
            category = Category.objects.get(slug=slug)
            return category.products.all()
        except Category.DoesNotExist:
            raise HttpError(404, "Category does not exists")
