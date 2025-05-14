from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

UserModel = get_user_model()


class UsernameOrEmailBackend(ModelBackend):
    """
    Authenticate using either username, email or phone number.
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        user = None
        try:
            user = UserModel.objects.get(username=username)
        except UserModel.DoesNotExist:
            try:
                user = UserModel.objects.get(email=username)
            except UserModel.DoesNotExist:
                pass
                # try:
                #     user = UserModel.objects.get(phone_number=username)  # assumes you have this field
                # except UserModel.DoesNotExist:
                #     pass

        if user and user.check_password(password):
            return user
        return None
