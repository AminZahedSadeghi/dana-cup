from ninja.errors import HttpError
from ninja_extra import api_controller, ControllerBase, route
from ninja_jwt.authentication import JWTAuth

from orders.models import Order
from products.models import Product, Category, ProductColor
from .schemas import ProductListOutSchema, CategoriesListOutSchema, CategoryCreateInSchema, CategoryUpdateInSchema, ProductCreateInSchema, \
    ProductUpdateInSchema, OrderListOutSchema, OrderUpdateInSchema
from django.db import IntegrityError


@api_controller('/admin', tags=['Admin'], auth=JWTAuth())
class AdminController(ControllerBase):
    @route.get('/products', response=list[ProductListOutSchema], url_name='', description='')
    def product_list(self):
        return Product.objects.all()

    @route.post('/products', response={204: None}, url_name='', description='')
    def product_create(self, data: ProductCreateInSchema):
        try:
            try:
                category = Category.objects.get(slug=data.category_slug)
            except Category.DoesNotExist:
                raise HttpError(404, 'Category does not exists')

            try:
                Product.objects.get(title=data.title)
                raise HttpError(404, f'Already product with {data.title} title exists !')
            except Product.DoesNotExist:
                pass

            product = Product.objects.create(
                title=data.title,
                price=data.price,
                discount_percentage=data.discount_percentage,
                category_id=category.id,
                description=data.description,
            )
            if data.tags:
                product.tags.add(*data.tags)

            if data.colors:
                for color in data.colors:
                    colors = ProductColor.objects.get_or_create(name=color.name, color=color.color)
                    product.colors.add(*colors)

            return 204, {}
        except IntegrityError:
            return 204, {}

    @route.put('/products/{pk}', response={204: None}, url_name='', description='')
    def product_update(self, pk: int, data: ProductUpdateInSchema):
        try:
            category = Category.objects.get(slug=data.category_slug)
        except Category.DoesNotExist:
            raise HttpError(404, 'Category does not exists')

        try:
            product = Product.objects.get(id=pk)
            product.title = data.title
            product.price = data.price
            product.description = data.description
            product.category = category

            if data.colors:
                for color in data.colors:
                    colors = ProductColor.objects.get_or_create(name=color.name, color=color.color)
                product.colors.clear()
                product.colors.add(*colors)

            if data.tags:
                product.tags.clean()
                product.tags.add(*data.tags)

        except Product.DoesNotExist:
            raise HttpError(404, 'This product does not exists')
        return 204, {}

    @route.delete('/products/{pk}', response={204: None}, url_name='', description='')
    def product_delete(self, pk: int):
        try:
            product = Product.objects.get(id=pk)
            product.delete()
        except Product.DoesNotExist:
            raise HttpError(404, 'This product does not exists')
        return 204, {}

    @route.get('/categories', response=list[CategoriesListOutSchema], url_name='', description='')
    def category_list(self):
        return Category.objects.all()

    @route.post('/categories', response={204: None}, url_name='', description='')
    def category_create(self, data: CategoryCreateInSchema):
        Category.objects.get_or_create(title=data.title, slug=data.slug)
        return 204, {}

    @route.put('/categories/{slug}', response={204: None}, url_name='', description='')
    def category_update(self, slug: str, data: CategoryUpdateInSchema):
        try:
            category = Category.objects.get(slug=slug)
            category.title = data.title
            category.slug = data.slug
            category.save()
        except Category.DoesNotExist:
            raise HttpError(404, 'This category does not exists')
        return 204, {}

    @route.delete('/categories/{slug}', response={204: None}, url_name='', description='')
    def category_delete(self, slug: str):
        try:
            category = Category.objects.get(slug=slug)
            category.delete()
        except Category.DoesNotExist:
            raise HttpError(404, 'This category does not exists')
        return 204, {}

    @route.get('/orders', response=list[OrderListOutSchema], url_name='', description='')
    def order_list(self):
        return Order.objects.all()

    @route.put('/orders/{pk}', response={204: None}, url_name='', description='')
    def order_update_status(self, pk: int, data: OrderUpdateInSchema):
        try:
            order = Order.objects.get(id=pk)
            order.status = data.status
            order.save()
        except Order.DoesNotExist:
            raise HttpError(404, 'This order does not exists')
        return 204, {}
