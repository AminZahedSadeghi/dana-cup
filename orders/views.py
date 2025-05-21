from ninja_extra import api_controller, ControllerBase, route

from .models import Order, OrderItem
from ninja_jwt.authentication import JWTAuth
from .schemas import OrderCreateInSchema, OrderListOutSchema
from ninja.errors import HttpError


@api_controller('/orders', tags=['Order'], auth=JWTAuth())
class OrderController(ControllerBase):
    @route.post('', response={204: None}, url_name='orders@create', description='Create new order')
    def order_create(self, data: OrderCreateInSchema):
        user = self.context.request.user
        cart = user.cart

        if cart.is_empty:
            raise HttpError(406, 'سبد خرید خالی است !')

        order = Order.objects.create(
            user=user, full_name=data.full_name, postal_code=data.postal_code, address=data.address,
            payment_type=data.payment_type
        )
        for cart_item in user.cart.items.all():
            OrderItem.objects.create(
                order_id=order.id, quantity=cart_item.quantity, product_id=cart_item.product_id,
                price=cart_item.product.discount_price
            )
        user.cart.clear()
        return 204, {}

    @route.get('', response=list[OrderListOutSchema], url_name='orders@list', description='List of user orders')
    def user_orders(self):
        user = self.context.request.user
        return Order.objects.filter(user=user)
