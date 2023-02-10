from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model

class authLogin(BaseBackend):
    def authenticate(self, request, email=None, password=None):
        UserModel = get_user_model()
        try:
            # retrieve the user from the existing table based on the provided username
            user = UserModel.objects.get(email=email)
            if user.check_password(password):
                return user
        except UserModel.DoesNotExist:
            return None

    def get_user(self, user_id):
        UserModel = get_user_model()
        try:
            # retrieve the user from the existing table based on the user_id
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None