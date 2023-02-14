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
        email = request.data['email']
        password = request.data['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            response = Response({"message": "Login successful."}, status.HTTP_200_OK)
            response.set_cookie("sessionid", request.session.session_key, max_age=3)
            return response
        else:
            return Response({'error':'Unauthorized'},status=status.HTTP_401_UNAUTHORIZED)





class LogoutPoint(APIView):
    def delete(self, request, format=None):
        try:
            request.session.delete()
        except KeyError:
            pass
        return Response(status=status.HTTP_200_OK)


#class based (Create, Update, Delete)
class RoleClass(generics.GenericAPIView, mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, mixins.RetrieveModelMixin):
    serializer_class = RoleTableSerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = RoleTable.objects.all()
    lookup_field = 'role_id'

    def get(self, request, role_id=None):
        if role_id:
            return self.retrieve(request)
        else:
            return self.list(request)


    def post(self, request):
        return self.create(request)

    def put(self, request, role_id=None):
        return self.update(request, role_id)

    def delete(self, request, role_id=None):
        return self.destroy(request, role_id)

class CategoryClass(generics.GenericAPIView, mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, mixins.RetrieveModelMixin):
    authentication_classes = [SessionAuthentication]
    serializer_class = CategorySerializer
    queryset = CategoryTable.objects.all()
    lookup_field = 'category_id'

    def get(self, request, category_id=None):
        if category_id:
            return self.retrieve(request)
        else:
            return self.list(request)

    def post(self, request):
        return self.create(request)


    def put(self, request, category_id=None):
        return self.update(request, category_id)

    def delete(self, request, category_id=None):
        return self.destroy(request, category_id)

class InventoryClass(generics.GenericAPIView, mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, mixins.RetrieveModelMixin):
    serializer_class = InventoryTableSerializer
    queryset = InventoryTable.objects.all()
    lookup_field = 'item_code'

    def get(self, request, item_code=None):
        if item_code:
            return self.retrieve(request)
        else:
            return self.list(request)

    def post(self, request):
        return self.create(request)

    def put(self, request, item_code=None):
        return self.update(request, item_code)

    def delete(self, request, item_code=None):
        return self.destroy(request, item_code)

class HistoryClass(generics.GenericAPIView, mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, mixins.RetrieveModelMixin):
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

class reservationsClass(generics.GenericAPIView, mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, mixins.RetrieveModelMixin):
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
