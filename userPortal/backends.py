from django.contrib.auth.backends import BaseBackend
from userPortal.models import UserTable
from django.contrib.auth.hashers import PBKDF2PasswordHasher

class userAuth(BaseBackend):
    def authenticate(self, request, email=None, password=None):
        entered_Password = password
        hasher = PBKDF2PasswordHasher()
        try:
            user = UserTable.objects.get(email=email)
            if hasher.verify(entered_Password, user.user_password):
                request.session['email'] = email
                request.session['role'] = user.role_id
                return user
            else:
                return None
        except UserTable.DoesNotExist:
            return None


    def get_user(self, user_id):
        try:
            return UserTable.objects.get(email=user_id)
        except UserTable.DoesNotExist:
            return None
