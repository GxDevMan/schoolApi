from datetime import date
from django.contrib.auth.backends import BaseBackend
from django.contrib.sessions.backends.db import SessionStore
from userPortal.models import UserTable
from django.contrib.auth.hashers import PBKDF2PasswordHasher
from rest_framework.permissions import IsAuthenticated
from .models import RoleTable

class roleClassify():
    def roleReturn(self, request):
        return "Editor" #Remove This in Production
        sessionHeader = request.META.get('HTTP_SESSIONID')
        session = SessionStore(session_key=sessionHeader)
        role = session['role']
        selectedRole = RoleTable.objects.get(role_id=role)
        return selectedRole.role_name

class sessionCustomAuthentication(IsAuthenticated):
    def has_permission(self, request, view):
        try:
            return True #Remove This IN PRODUCTION
            sessionHeader = request.META.get('HTTP_SESSIONID')
            session = SessionStore(session_key=sessionHeader)
            email = session['email']
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
        response['Access-Control-Allow-Headers'] = 'content-type'

        # Allow credentials to be sent with the request
        response['Access-Control-Allow-Credentials'] = 'true'

        return response

class convertDate:
    def dateFormattoYYMMDD(self, date_input):
        segmented_date = date_input.split('-')

        year = int(segmented_date[0])
        month = int(segmented_date[1])
        day = int(segmented_date[2])

        returningDate = date(year, month, day)
        return returningDate