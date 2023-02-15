from django.contrib.auth import authenticate
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db import connections
from .models import UserTable, InventoryTable, ReservationTable, CategoryTable
from .models import RoleTable, HistoryTable
from rest_framework.decorators import api_view, APIView
from .serializers import \
    UserTableSerializer, \
    InventoryTableSerializer,\
    RoleTableSerializer, \
    ReservationSerializer, \
    CategorySerializer, \
    HistorySerializer
from rest_framework import generics, status
from rest_framework import mixins

#function based
@api_view(['GET'])
def returnListofRoles(request):
    if request.method == 'GET':
        try:
            db_conn = connections['default']
        except:
            response = "failed"
            return Response(response)

        cursor = db_conn.cursor()
        cursor.execute("SELECT * FROM schooldb.role_table")
        roles = []

        for row in cursor.fetchall():
            Role1 = RoleTable(role_id=row[0], role_name=row[1])
            roles.append(Role1)

        querySet = RoleTable.objects.bulk_create(roles, ignore_conflicts=True)

        data = []

        for Role2 in querySet:
            data.append(
                {
                    'role_id': Role2.role_id,
                    'role_name': Role2.role_name
                }
            )
        return Response(data)


@api_view(['GET'])
def roles(request):
    if request.method == 'GET':
        roles = RoleTable.objects.all()
        serializer = RoleTableSerializer(roles, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def viewUsers(request):

    if request.method == 'GET':
        users = UserTable.objects.all()
        serializer = UserTableSerializer(users, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def viewItems(request):
    if request.method == 'GET':
        items = InventoryTable.objects.all()
        serializer = InventoryTableSerializer(items, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def testFunction(request):
    if request.method == 'GET':
        try:
            print(request.session['email'])
            print(request.session['role'])
        except:
            print("error")
    return Response(status=status.HTTP_200_OK)


#authenticate
class LoginPoint(APIView):
    def post(self, request, format=None):
        try:
            email = request.data['email']
            password = request.data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                response = Response({"message": "Login successful."}, status.HTTP_200_OK)
                response.set_cookie("sessionid", request.session.session_key, max_age=3)
                return response
            else:
                return Response({'error':'Unauthorized'},status=status.HTTP_401_UNAUTHORIZED)
        except:
            return Response({'error':'Insufficient Credentials'}, status=status.HTTP_401_UNAUTHORIZED)





class LogoutPoint(APIView):
    def delete(self, request, format=None):
        try:
            request.session.delete()
            return Response(status=status.HTTP_200_OK)
        except KeyError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class roleClassify():
    def roleReturn(self, request):
        role = request.session['role']
        selectedRole = RoleTable.objects.get(role_id=role)
        return selectedRole.role_name



#class based (Create, Update, Delete)
class RoleClass(generics.GenericAPIView, mixins.ListModelMixin):
    serializer_class = RoleTableSerializer
    queryset = RoleTable.objects.all()
    roleLookup = roleClassify()

    def get(self, request):
        strRole = self.getRole(request)
        if strRole == "Editor" or strRole == "Admin":
            return self.list(request)
        else:
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

    def getRole(self, request):
        try:
            lookUpRole = self.roleLookup.roleReturn(request)
            return lookUpRole
        except:
            return ""

#     def post(self, request):
#         strRole = self.roleLookup.roleReturn(request)
#         if strRole == "Editor" or strRole == "Admin":
#             return self.create(request)
#         else:
#             return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
#
#     def put(self, request, role_id=None):
#         strRole = self.roleLookup.roleReturn(request)
#         if strRole == "Editor" or strRole == "Admin":
#             return self.update(request, role_id)
#         else:
#             return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
#
#     def delete(self, request, role_id=None):
#         strRole = self.roleLookup.roleReturn(request)
#         if strRole == "Editor" or strRole == "Admin":
#             return self.destroy(request, role_id)
#         else:
#             return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)


class CategoryClass(generics.GenericAPIView, mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, mixins.RetrieveModelMixin, mixins.ListModelMixin):
    authentication_classes = [SessionAuthentication]
    serializer_class = CategorySerializer
    queryset = CategoryTable.objects.all()
    lookup_field = 'category_id'
    roleLookup = roleClassify()

    def get(self, request, category_id=None):
        strRole = self.getRole(request)
        if strRole == "Editor" or strRole == "Admin" or strRole == "User":
            if category_id:
                return self.retrieve(request)
            else:
                return self.list(request)
        else:
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

    def post(self, request):
        strRole = self.getRole(request)
        if strRole == "Editor" or strRole == "Admin":
            return self.create(request)
        else:
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)


    def put(self, request, category_id=None):
        strRole = self.getRole(request)
        if strRole == "Editor" or strRole == "Admin":
            return self.update(request, category_id)
        else:
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

    def delete(self, request, category_id=None):
        strRole = self.getRole(request)
        if strRole == "Editor" or strRole == "Admin":
            return self.destroy(request, category_id)
        else:
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

    def getRole(self, request):
        try:
            lookUpRole = self.roleLookup.roleReturn(request)
            return lookUpRole
        except:
            return ""

class InventoryClass(generics.GenericAPIView, mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, mixins.RetrieveModelMixin, mixins.ListModelMixin):
    serializer_class = InventoryTableSerializer
    queryset = InventoryTable.objects.all()
    lookup_field = 'item_code'
    roleLookup = roleClassify()

    def get(self, request, item_code=None):
        strRole = self.getRole(request)
        if strRole == "Editor" or strRole == "Admin":
            if item_code:
                return self.retrieve(request)
            else:
                return self.list(request)
        else:
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

    def post(self, request):
        strRole = self.getRole(request)
        if strRole == "Editor" or strRole == "Admin":
            return self.create(request)
        else:
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

    def put(self, request, item_code=None):
        strRole = self.getRole(request)
        if strRole == "Editor" or strRole == "Admin":
            return self.update(request, item_code)

    def delete(self, request, item_code=None):
        strRole = self.getRole(request)
        if strRole == "Editor" or strRole == "Admin":
            return self.destroy(request, item_code)
        else:
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

    def getRole(self, request):
        try:
            lookUpRole = self.roleLookup.roleReturn(request)
            return lookUpRole
        except:
            return ""

class HistoryClass(generics.GenericAPIView, mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, mixins.RetrieveModelMixin, mixins.ListModelMixin):
    serializer_class = HistorySerializer
    queryset = HistoryTable.objects.all()
    lookup_field = 'history_id'

    def get(self, request, history_id=None):
        if history_id:
            return self.retrieve(request)
        else:
            return self.list(request)

    def post(self, request):
        return self.create(request)

    def put(self, request, history_id=None):
        return self.update(request, history_id)

    def delete(self, request, history_id=None):
        return self.destroy(request, history_id)

class reservationsClass(generics.GenericAPIView, mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, mixins.RetrieveModelMixin, mixins.ListModelMixin):
    serializer_class = ReservationSerializer
    queryset = ReservationTable.objects.all()
    lookup_field = 'reservation_id'

    def get(self, request, reservation_id=None):
        if reservation_id:
            return self.retrieve(request)
        else:
            return self.list(request)

    def post(self, request):
        return self.create(request)

    def put(self, request, reservation_id=None):
        return self.update(request, reservation_id)

    def delete(self, request, reservation_id=None):
        return self.destroy(request, reservation_id)
