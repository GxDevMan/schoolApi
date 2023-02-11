from django.contrib.auth.backends import BaseBackend
from userPortal.models import UserTable

class userAuth(BaseBackend):
    def authenticate(self, request, email=None, password=None):
        # queryset = UserTable.objects.filter(email=email).values()
        # role = 0
        # dbPass = ""
        #
        # for dataIn in queryset:
        #     dbPass = dataIn['password']
        #     role = dataIn['role_id']

        try:
            user = UserTable.objects.get(email=email, password=password)
            request.session['role'] = user.role_id
            return user
        except UserTable.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return UserTable.objects.get(email=user_id)
        except UserTable.DoesNotExist:
            return None
