from django.contrib.auth import authenticate
from django.http import JsonResponse
from rest_framework.authentication import SessionAuthentication
from django.db.models import Q
from .backends import roleClassify
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
import pytz
import datetime

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
def historyReport(request):
    if request.method == 'GET':
        getRole = roleClassify()
        strRole = getRole.roleReturn(request)
        if strRole == "Admin" or strRole == "Editor":

            filteredData = HistoryTable.objects.all()
        else:
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
def viewItemsthatCanBeReserved(request):
    if request.method == 'GET':
        try:
            getRole = roleClassify()
            strRole = getRole.roleReturn(request)
            today = datetime.datetime.today()
            query = InventoryTable.objects.filter(
                ~Q(item_code__in=ReservationTable.objects.filter(date_of_expiration__gte=today).filter(claim=0).values_list('item_code', flat=True)) &
                ~Q(item_code__in=HistoryTable.objects.filter(date_out__isnull=True).values_list('item_code',flat=True))).filter(status="Available")
            siftedData = list(query.values())
            return Response(siftedData)
        except Exception as e:
            return Response({'error':'Unauthorized Access'}, status=status.HTTP_401_UNAUTHORIZED)
    return Response(status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
def roles(request):
    if request.method == 'GET':
        roles = RoleTable.objects.all()
        serializer = RoleTableSerializer(roles, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def testFunction(request):
    if request.method == 'GET':
        try:
            print("")
            # <year>-<month>-<day>-<hour>-<minute>-<second>-<microsecond>
            # print(request.GET.get('start_date'))
            # print(request.GET.get('end_date'))
            #
            # start_date = datetime.datetime(2021, 1, 20, 20, 8, 7, 127325, tzinfo=pytz.UTC)
            # end_date = datetime.datetime(2024, 3, 20, 20, 8, 7, 127325, tzinfo=pytz.UTC)
            #
            # queryset = HistoryTable.objects.filter(date_out__range=(start_date, end_date)).order_by('-date_out')
            # data = HistorySerializer(queryset, many=True).data
            #
            # print(request.session['email'])
            # print(request.session['role'])
            # return Response(data)
            today = datetime.datetime.today()
            testQuery = InventoryTable.objects.filter(
                ~Q(item_code__in=ReservationTable.objects.filter(date_of_expiration__gte=today).filter(claim=0).values_list('item_code', flat=True)) &
                ~Q(item_code__in=HistoryTable.objects.filter(date_out__isnull=True).values_list('item_code',flat=True))).filter(status="Available")
            siftedData = list(testQuery.values())
            return Response(siftedData)
        except Exception as e:
            print(e)
            return Response({'error':'Internal Error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response(status=status.HTTP_200_OK)


#authenticate
class LoginPoint(APIView):
    def post(self, request, format=None):
        try:
            email = request.data['email']
            password = request.data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                request.session['email'] = email
                request.session['role'] = user.role_id
                response = Response({"message": "Login successful.",
                                     "role": request.session['role']}, status.HTTP_200_OK)
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

class UsersClass(generics.GenericAPIView, mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, mixins.RetrieveModelMixin, mixins.ListModelMixin):
    serializer_class = UserTableSerializer
    queryset = UserTable.objects.all()
    lookup_field = 'email'
    roleLookup = roleClassify()

    def get(self, request, email=None):
        strRole = self.getRole(request)
        if strRole == "Editor" or strRole == "Admin":
            if email:
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

    def put(self, request, email=None):
        strRole = self.getRole(request)
        if strRole == "Editor" or strRole == "Admin":
            return self.update(request, email)

    def delete(self, request, email=None):
        strRole = self.getRole(request)
        if strRole == "Editor" or strRole == "Admin":
            return self.destroy(request, email)
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
