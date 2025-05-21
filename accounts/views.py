from ninja_extra import api_controller, ControllerBase, route

from cart.models import Cart
from .exceptions import UsernameAlreadyExists406, UsernameAlreadyExists
from .models import User
from .schemas import RegisterInSchema, AuthOutSchema
from ninja_jwt.authentication import JWTAuth


@api_controller('/customers', tags=['Auth'], auth=None)
class AccountController(ControllerBase):
    @route.get('', response=AuthOutSchema, url_name='auth', description='get profile info', auth=JWTAuth())
    def profile_info(self):
        return {'username': self.context.request.user.username}

    @route.post('/register', response={204: None, 406: UsernameAlreadyExists406}, url_name='accounts@register', description='Register user',
                auth=None)
    def register(self, data: RegisterInSchema):
        try:
            User.objects.get(username=data.username)
            raise UsernameAlreadyExists
        except User.DoesNotExist:
            user = User.objects.create_user(username=data.username, password=data.password)
            Cart.objects.create(user=user)

        return 204, {}
