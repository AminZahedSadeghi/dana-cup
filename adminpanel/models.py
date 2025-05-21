from django.db import models

from ninja_extra import api_controller, ControllerBase, route


@api_controller('/admin', tags=['Admin'])
class AdminLoginController(ControllerBase):
    pass
