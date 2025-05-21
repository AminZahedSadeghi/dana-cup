from ninja.errors import HttpError
from ninja_extra import api_controller, ControllerBase, route
from ninja_jwt.authentication import JWTAuth

from .models import CartItem
from .schemas import CartAddItemInSchema, CartItemListOutSchema, CartInfoSchema, CartItemUpdateInSchema


@api_controller('/cart', tags=['Cart'], auth=JWTAuth())
class CartController(ControllerBase):

    @route.post('', response={204: None}, url_name='cart@list', description='Get cart list')
    def add_cart_item(self, data: CartAddItemInSchema):
        cart = self.context.request.user.cart
        try:
            CartItem.objects.create(cart_id=cart.id, quantity=data.quantity, product_id=data.product_id)
        except:
            raise HttpError(404, 'Product id does not exists')

        return 204, {}

    @route.get('', response=list[CartItemListOutSchema], url_name='cart@list', description='Get cart list')
    def cart_items(self):
        cart = self.context.request.user.cart
        return cart.items.all()

    @route.get('/info', response=CartInfoSchema, url_name='cart@info', description='Get cart list')
    def cart_info(self):
        cart = self.context.request.user.cart
        return cart

    @route.put('/{item_id}', response={204: None}, url_name='cart@cart_item_update', description='Update quantity of cart item')
    def cart_item_update_quantity(self, item_id: int, data: CartItemUpdateInSchema):
        cart = self.context.request.user.cart

        try:
            cart_item = CartItem.objects.get(id=item_id, cart_id=cart.id)
            cart_item.quantity = data.quantity
            cart_item.save()
        except CartItem.DoesNotExist:
            raise HttpError(404, 'Cart Item does not exists')

        return 204, {}

    @route.delete('/{item_id}', response={204: None}, url_name='cart@cart_item_delete', description='Delete cart item')
    def cart_item_delete(self, item_id: int):
        cart = self.context.request.user.cart
        try:
            CartItem.objects.get(id=item_id, cart_id=cart.id).delete()
        except CartItem.DoesNotExist:
            raise HttpError(404, 'Cart Item does not exists')

        return 204, {}
