from ninja_extra import api_controller, ControllerBase, route
from .models import User
from .schemas import RegisterInSchema
from .exceptions import UsernameAlreadyExists406, UsernameAlreadyExists


@api_controller('/auth', tags=['Auth'], auth=None)
class AccountController(ControllerBase):
    @route.post('/register', response={204: None, 406: UsernameAlreadyExists406}, url_name='accounts@register', description='Register user')
    def register(self, data: RegisterInSchema):
        try:
            User.objects.get(username=data.username)
            raise UsernameAlreadyExists
        except User.DoesNotExist:
            User.objects.create_user(username=data.username, password=data.password)

        return 204, {}
