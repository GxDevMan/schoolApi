from django.contrib.auth.backends import BaseBackend
from userPortal.models import UserTable
from django.contrib.auth.hashers import PBKDF2PasswordHasher
from .models import RoleTable

class userAuth(BaseBackend):
    def authenticate(self, request, email=None, password=None):
        entered_Password = password
        hasher = PBKDF2PasswordHasher()
        try:
            user = UserTable.objects.get(email=email)
            if hasher.verify(entered_Password, user.user_password):
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


class roleClassify():
    def roleReturn(self, request):
        role = request.session['role']
        selectedRole = RoleTable.objects.get(role_id=role)
        return selectedRole.role_name
