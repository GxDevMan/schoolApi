from django.contrib.auth import authenticate
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.sessions.models import Session
from django.shortcuts import get_object_or_404, render
from django.db.models import Q
from .backends import sessionCustomAuthentication
from .backends import roleClassify
from rest_framework.response import Response
from .models import UserTable, InventoryTable, ReservationTable, CategoryTable
from .models import RoleTable, HistoryTable
from rest_framework.decorators import api_view, APIView, permission_classes
from .serializers import \
    UserTableSerializer, \
    InventoryTableSerializer, \
    RoleTableSerializer, \
    ReservationSerializer, \
    CategorySerializer, \
    HistorySerializer, \
    changePassSerializer,\
    specialInventorySerializer, pendingReservationSerializer, specialHistorySerializer, \
    multipleItemInsertSerializer, specialHistoryReportSerializer, specialReservationSerializer, \
    multipleItemUpdateSerializer, specialInsertReservationSerializer, specialInsertHistorySerializer, textPeopleFindSerializer
from rest_framework import generics, status
from rest_framework import mixins
from .backends import convertDate
import datetime

#function based
# @api_view(['GET'])
# def returnListofRoles(request):
#     if request.method == 'GET':
#         try:
#             db_conn = connections['default']
#         except:
#             response = "failed"
#             return Response(response)
#
#         cursor = db_conn.cursor()
#         cursor.execute("SELECT * FROM schooldb.role_table")
#         roles = []
#
#         for row in cursor.fetchall():
#             Role1 = RoleTable(role_id=row[0], role_name=row[1])
#             roles.append(Role1)
#
#         querySet = RoleTable.objects.bulk_create(roles, ignore_conflicts=True)
#
#         data = []
#
#         for Role2 in querySet:
#             data.append(
#                 {
#                     'role_id': Role2.role_id,
#                     'role_name': Role2.role_name
#                 }
#             )
#         return Response(data)

#DEPRECIATED
# @api_view(['GET'])
# @permission_classes([sessionCustomAuthentication])
# def historyReport(request):
#     if request.method == 'GET':
#         getRole = roleClassify()
#         strRole = getRole.roleReturn(request)
#         if strRole == "Admin" or strRole == "Editor":
#             filteredData = HistoryTable.objects.filter(date_out__isnull=False).filter(date_out__lte=datetime.datetime.today()).select_related('item_code__category').select_related('email')
#             serializer = specialHistoryReportSerializer(filteredData, many=True)
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         else:
#             return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
@permission_classes([sessionCustomAuthentication])
def pendingReservation(request):
    if request.method == 'GET':
        try:
            email = request.session['email']
            today = datetime.datetime.today()
            filteredData = ReservationTable.objects.filter(email=email).filter(claim=0).filter(date_of_expiration__gte=today).select_related('item_code')
            serializer = pendingReservationSerializer(filteredData, many=True)
            return Response(serializer.data)
        except:
            return Response({'message':'exception type'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['DELETE'])
@permission_classes([sessionCustomAuthentication])
def clearAllreservations(request):
    if request.method == 'DELETE':
        getRole = roleClassify()
        strRole = getRole.roleReturn(request)
        if strRole == "Editor":
            try:
                today = datetime.datetime.today()
                filteredData = ReservationTable.objects.filter(Q(claim=1) | Q(date_of_expiration__lt=today))
                filteredData.delete()
                return Response({'Message': 'Unecessarry reservations deleted'})
            except:
                return Response({'Message': 'Exception Occured'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({'message': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
@permission_classes([sessionCustomAuthentication])
def viewItemsthatCanBeReserved(request):
    if request.method == 'GET':
        try:
            getRole = roleClassify()
            today = datetime.datetime.today()
            query = InventoryTable.objects.filter(
                ~Q(item_code__in=ReservationTable.objects.filter(date_of_expiration__gte=today).filter(claim=0).values_list('item_code', flat=True)) &
                ~Q(item_code__in=HistoryTable.objects.filter(date_out__isnull=True).values_list('item_code',flat=True))).filter(status="Available").select_related('category')
            serializer = specialInventorySerializer(query, many=True)
            return Response(serializer.data)
        except:
            return Response({'message':'Exception Occured'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([sessionCustomAuthentication])
def updatePass(request):
    if request.method == 'PUT':
        try:
            getRole = roleClassify()
            strRole = getRole.roleReturn(request)
            sessionemail = request.session['email']
            #password = request.data['user_password'] new password
            old_password = request.data['old_password']

            new_password = request.data['new_password']
            new_password2 = request.data['user_password']

            if new_password != new_password2:
                return Response({'message':'password does not match'}, status=status.HTTP_409_CONFLICT)

            selectedData = get_object_or_404(UserTable, email=sessionemail)
            user = authenticate(request, email=sessionemail, password=old_password)
            if user is not None:
                serializer = changePassSerializer(selectedData, request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response({'message': 'password successfully changed'})
            else:
                return Response({'error': 'password does not match the old password'}, status=status.HTTP_404_NOT_FOUND)
        except:
            return Response({'message': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)


def frontEnd(request):
    return render(request, 'index.html')

@api_view(['GET'])
def testFunction(request):
    if request.method == 'GET':

        try:
            pass
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
            # today = datetime.datetime.today()
            # testQuery = InventoryTable.objects.filter(
            #     ~Q(item_code__in=ReservationTable.objects.filter(date_of_expiration__gte=today).filter(
            #         claim=0).values_list('item_code', flat=True)) & ~Q(item_code__in=HistoryTable.objects.filter(date_out__isnull=True).values_list('item_code', flat=True))).filter(status="Available").select_related('category')
            # siftedData = list(
            #     testQuery.values('item_code', 'item_name', 'item_condition', 'status', 'category__category_name'))
            # return Response(siftedData)

        except Exception as e:
            print(e)
            return Response({'error':'Internal Error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response(status=status.HTTP_200_OK)

@permission_classes([sessionCustomAuthentication])
@api_view(['GET'])
def textPeople(request):
    if request.method == 'GET':
        today = datetime.datetime.today()
        query = HistoryTable.objects.filter(date_out__isnull=True).filter(due_date__lt=today)
        serializer = textPeopleFindSerializer(query, many=True)
        data = serializer.data

        for i in data:
            print(i['email']['phone_number'])

        return Response(serializer.data)

#authenticate
class LoginPoint(APIView):
    def post(self, request, format=None):
        email = request.data['email']
        password = request.data['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            session = SessionStore()

            session['email'] = email
            session['role'] = user.role_id
            session.create()

            queryset = RoleTable.objects.filter(role_id=user.role_id)
            serializer = RoleTableSerializer(queryset, many=True)

            response = Response({"message": "Login successful.",
                                 "role": serializer.data[0]['role_name'],
                                 "sessionid": session.session_key}, status.HTTP_200_OK)
            response.set_cookie('sessionid', session.session_key, httponly=True)
            return response
        else:
            return Response({'error':'Unauthorized'},status=status.HTTP_401_UNAUTHORIZED)

@permission_classes([sessionCustomAuthentication])
class LogoutPoint(APIView):
    def delete(self, request, format=None):
        try:
            request.session.delete()
            return Response(status=status.HTTP_200_OK)
        except KeyError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([sessionCustomAuthentication])
def logoutAllUsers(request):
    if request.method == 'DELETE':
        getRole = roleClassify()
        strRole = getRole.roleReturn(request)
        if strRole == "Editor":
            Session.objects.all().delete()
            return Response({'Message': 'All Users Logged out'})
        else:
            return Response({'message':'Unauthorized'},status=status.HTTP_401_UNAUTHORIZED)

#Class Based Views
class countStatus(generics.GenericAPIView):
    permission_classes = [sessionCustomAuthentication]
    roleLookup = roleClassify()

    def get(self, request):
        strRole = self.roleLookup.roleReturn(request)
        if strRole == "Editor" or strRole == "Admin":
            working = InventoryTable.objects.filter(item_condition="Working").count()
            maintenance = InventoryTable.objects.filter(item_condition="Maintenance").count()
            retired = InventoryTable.objects.filter(item_condition="Retired").count()
            damaged = InventoryTable.objects.filter(item_condition="Damaged").count()
            lost = InventoryTable.objects.filter(item_condition="Lost").count()

            data = {'working': working,
                    'maintenance': maintenance,
                    'retired': retired,
                    'damaged': damaged,
                    'lost': lost}
            return Response(data)

        else:
            return Response({'message':'UnAuthorized access'}, status=status.HTTP_403_FORBIDDEN)


#class based (Create, Update, Delete)
class RoleClass(generics.GenericAPIView, mixins.ListModelMixin):
    permission_classes = [sessionCustomAuthentication]
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

class CategoryClass(generics.GenericAPIView, mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, mixins.RetrieveModelMixin, mixins.ListModelMixin):
    permission_classes = [sessionCustomAuthentication]
    serializer_class = CategorySerializer
    queryset = CategoryTable.objects.all()
    lookup_field = 'category_id'
    roleLookup = roleClassify()

    def get(self, request, category_id=None):
        if category_id:
            return self.retrieve(request)
        else:
            return self.list(request)

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
    permission_classes = [sessionCustomAuthentication]
    queryset = InventoryTable.objects.all()
    lookup_field = 'item_code'
    lookup_url_kwarg = 'item_code'
    filter_lookup_field = 'filter'
    filter_lookup_url_kwarg = 'filter'
    roleLookup = roleClassify()
    serializer_class = InventoryTableSerializer

    def put(self, request, item_code=None):
        strRole = self.getRole(request)
        if strRole == "Editor" or strRole == "Admin":
            return self.update(request, item_code)
        else:
            return Response({'message':'Unauthorized'}, status=status.HTTP_200_OK)

    def get(self, request, item_code=None, filter=None):
        strRole = self.getRole(request)
        if strRole == "Editor" or strRole == "Admin":
            if item_code is not None:
                queryset = self.get_queryset().filter(item_code=item_code)
                serializer = specialInventorySerializer(queryset, many=True)
                response = Response(serializer.data)
                return response

            if filter is not None:
                queryset = self.get_queryset().filter(item_condition=filter)
                serializer = specialInventorySerializer(queryset, many=True)
                response = Response(serializer.data)
                return response
            else:
                serializer = specialInventorySerializer(self.get_queryset(), many=True)
                response = Response(serializer.data)
                return response
        else:
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

    def post(self, request):
        strRole = self.getRole(request)
        if strRole == "Editor" or strRole == "Admin":
            #note data sent should be in brackets
            serializer = multipleItemInsertSerializer(data=request.data, many=True)
            if serializer.is_valid(raise_exception=False):
                self.perform_create(serializer)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

    def patch(self, request):
        strRole = self.getRole(request)
        if strRole == "Editor" or strRole == "Admin":
            serializer = multipleItemUpdateSerializer(data=request.data, many=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message':'Unauthorized'}, status=status.HTTP_200_OK)

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
    permission_classes = [sessionCustomAuthentication]
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
            serializer = UserTableSerializer(data=request.data, many=True)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_200_OK)
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
    permission_classes = [sessionCustomAuthentication]
    serializer_class = HistorySerializer
    queryset = HistoryTable.objects.all()
    roleLookup = roleClassify()
    dateConversion = convertDate()
    lookup_field = 'history_id'
    lookup_url_kwarg = 'history_id'
    startdate_lookup_field = 'start_date'
    startdate_lookup_url_kwarg = 'start_date'
    enddate_lookup_field = 'end_date'
    endate_lookup_url_kwarg = 'end_date'

    def put(self, request, history_id=None):
        return self.update(request, history_id)

    def get(self, request, history_id=None, start_date=None, end_date=None):
        strRole = self.getRole(request)
        if strRole == "Admin" or strRole == "Editor":
            if history_id:
                queryset = self.get_queryset().filter(history_id=history_id)
                serializer = specialHistorySerializer(queryset, many=True)
                return Response(serializer.data)
            if start_date and end_date:
                startingDate = self.dateConversion.dateFormattoYYMMDD(start_date)
                endingDate = self.dateConversion.dateFormattoYYMMDD(end_date)

                filteredData = HistoryTable.objects.filter(date_out__isnull=False).filter(
                    date_out__range=(startingDate, endingDate)).select_related('item_code__category').select_related(
                    'email')
                serializer = specialHistoryReportSerializer(filteredData, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                serializer = specialHistorySerializer(self.get_queryset().order_by('date_out'), many=True)
                return Response(serializer.data)
        else:
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)


    def post(self, request):
        strRole = self.getRole(request)
        if strRole == "Editor" or strRole == "Admin":
            try:
                serializer = specialInsertHistorySerializer(data=request.data, many=True)
                serializer.is_valid(raise_exception=True)

                self.perform_create(serializer)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Exception as e:
                print(e)
                return Response({'message': 'item is currently out'})

        else:
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

    def perform_create(self, serializer):
        item_code = serializer.data[0]['item_code']
        condition1 = InventoryTable.objects.filter(
            ~Q(item_code__in=HistoryTable.objects.filter(date_out__isnull=True).values_list('item_code', flat=True))).filter(item_code=item_code).filter(status="Available").select_related('category')
        condition2 = InventoryTable.objects.filter(status="Available").filter(item_code=item_code)
        if condition1.exists() and condition2.exists():
            serializer.save()
        else:
            return Response({'message': 'that item is currently out'}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, history_id=None):
        return self.destroy(request, history_id)

    def getRole(self, request):
        try:
            lookUpRole = self.roleLookup.roleReturn(request)
            return lookUpRole
        except:
            return ""

class reservationsClass(generics.GenericAPIView, mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, mixins.RetrieveModelMixin, mixins.ListModelMixin):
    permission_classes = [sessionCustomAuthentication]
    serializer_class = ReservationSerializer
    queryset = ReservationTable.objects.all()
    roleLookup = roleClassify()
    lookup_field = 'reservation_id'

    def get(self, request, reservation_id=None):
        strRole = self.getRole(request)
        if strRole == "Editor" or strRole == "Admin":
            if reservation_id:
                queryset = self.get_queryset().filter(reservation_id=reservation_id)
                serializer = specialReservationSerializer(queryset, many=True)
                return Response(serializer.data)
            else:
                serializer = specialReservationSerializer(self.get_queryset(), many=True)
                return Response(serializer.data)
        else:
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

    def post(self, request):
        serializer = specialInsertReservationSerializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def put(self, request, reservation_id=None):
        strRole = self.getRole(request)
        if strRole == "Editor" or strRole == "Admin":
            return self.update(request, reservation_id)
        else:
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

    def delete(self, request, reservation_id=None):
        return self.destroy(request, reservation_id)

    def perform_create(self, serializer):
        today = datetime.date.today()
        item_code = serializer.data[0]['item_code']
        condition1 = InventoryTable.objects.filter(
            ~Q(item_code__in=ReservationTable.objects.filter(date_of_expiration__gte=today).filter(claim=0).values_list(
                'item_code', flat=True)) & ~Q(item_code__in=HistoryTable.objects.filter(date_out__isnull=True).values_list('item_code', flat=True))).filter(item_code=item_code).filter(status="Available").select_related('category')
        condition2 = InventoryTable.objects.filter(status="Available").filter(item_code=item_code)
        if condition1.exists() and condition2.exists():
            serializer.save()
        else:
            pass

    def getRole(self, request):
        try:
            lookUpRole = self.roleLookup.roleReturn(request)
            return lookUpRole
        except:
            return ""


#special classes