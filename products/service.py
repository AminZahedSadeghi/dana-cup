from .models import Product, Category
from ninja.errors import HttpError
from django.db.models import QuerySet


class ProductService:
    @classmethod
    def product_list(cls) -> QuerySet[Product]:
        return Product.objects.all()

    @classmethod
    def product_detail(cls, pk: int) -> Product | None:
        try:
            return Product.objects.get(id=pk)
        except Product.DoesNotExist:
            raise HttpError(404, 'Product does not exists')
