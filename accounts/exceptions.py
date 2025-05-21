from ninja_extra.exceptions import APIException
from ninja_extra import status
from core.utils.common import create_exception_schema


class UsernameAlreadyExists(APIException):
    default_detail = "حساب کاربری با این مشخصات از قبل ثبت شده است !"
    status_code = status.HTTP_406_NOT_ACCEPTABLE


UsernameAlreadyExists406 = create_exception_schema('UsernameAlreadyExists406', UsernameAlreadyExists.default_detail)
