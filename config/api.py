from ninja_extra import NinjaExtraAPI
from ninja_jwt.controller import NinjaJWTDefaultController
from accounts.views import AccountController

api = NinjaExtraAPI(title="Blue IceBurner", version="0.1.0", urls_namespace="dana_cup")

api.register_controllers(NinjaJWTDefaultController)
api.register_controllers(AccountController)
