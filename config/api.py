from ninja_extra import NinjaExtraAPI
from ninja_jwt.controller import NinjaJWTDefaultController

from accounts.views import AccountController
from cart.views import CartController
from products.views import ProductController, CategoryController
from orders.views import OrderController
from adminpanel.views import AdminController

api = NinjaExtraAPI(title="Blue IceBurner", version="0.1.0", urls_namespace="dana_cup")

api.register_controllers(NinjaJWTDefaultController)
api.register_controllers(AccountController)
api.register_controllers(ProductController)
api.register_controllers(CategoryController)
api.register_controllers(CartController)
api.register_controllers(OrderController)
api.register_controllers(AdminController)
