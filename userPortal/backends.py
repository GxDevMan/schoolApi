from django.contrib.auth.backends import BaseBackend
from django.contrib.sessions.backends.db import SessionStore

from userPortal.models import UserTable
from django.contrib.auth.hashers import PBKDF2PasswordHasher
from rest_framework.permissions import  IsAuthenticated
from .models import RoleTable

class roleClassify():
    def roleReturn(self, request):
        sessionHeader = request.META.get('HTTP_SESSIONID')
        session = SessionStore(session_key=sessionHeader)
        role = session['role']
        print("Hello")
        selectedRole = RoleTable.objects.get(role_id=role)
        return selectedRole.role_name

class sessionCustomAuthentication(IsAuthenticated):
    def has_permission(self, request, view):
        try:
            sessionHeader = request.META.get('HTTP_SESSIONID')
            print(sessionHeader)
            session = SessionStore(session_key=sessionHeader)
            email = session['email']
            print(email)
            return True
        except:
            print("failed")
            return False

class sessionCustomAuthenticationTesting(IsAuthenticated):
    def has_permission(self, request, view):
        try:
            email = request.session['email']
            print(email)
            return True
        except:
            print("failed")
            return False

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

class CorsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Set the Access-Control-Allow-Origin header to the domain of the incoming request
        origin = request.headers.get('Origin')
        response['Access-Control-Allow-Origin'] = origin
        response['Access-Control-Allow-Headers'] = 'sessionid'
        response['Access-Control-Allow-Headers'] = 'Content-Type'

        # Allow credentials to be sent with the request
        response['Access-Control-Allow-Credentials'] = 'true'

        return response
