from userPortal.logic.historyLogic import historyLogic
from django.contrib.auth import authenticate
from .logic import functionLogic
from django.db.models import Q
from .logic.reservationLogic import reservationLogic
from .backends import sessionCustomAuthentication
from .backends import roleClassify
from django.utils import timezone
from rest_framework.response import Response
from .models import UserTable, InventoryTable, ReservationTable, CategoryTable
from .models import RoleTable, HistoryTable
from django.conf import settings
from rest_framework.decorators import api_view, APIView, permission_classes
from .serializers import \
    UserTableSerializer, \
    InventoryTableSerializer, \
    RoleTableSerializer, \
    ReservationSerializer, \
    CategorySerializer, \
    HistorySerializer, \
    specialInventorySerializer, specialHistorySerializer, \
    multipleItemInsertSerializer, specialReservationSerializer, \
    multipleItemUpdateSerializer, \
    textPeopleFindSerializer, specificUserHistorySerializer, specificUserReservationSerializer, \
    UserInsertTableSerializer
from rest_framework import generics, status
from rest_framework import mixins

@api_view(['GET'])
@permission_classes([sessionCustomAuthentication])
def pendingReservation(request):
    if request.method == 'GET':
        return functionLogic.getPendingreservation()

@api_view(['DELETE'])
@permission_classes([sessionCustomAuthentication])
def clearAllreservations(request):
    if request.method == 'DELETE':
        return functionLogic.clearReserveTable(request)

@api_view(['GET'])
@permission_classes([sessionCustomAuthentication])
def viewItemsthatCanBeReserved(request):
    if request.method == 'GET':
        return functionLogic.returnItemsviewReserve()

@api_view(['PUT'])
@permission_classes([sessionCustomAuthentication])
def updatePass(request):
    if request.method == 'PUT':
        return functionLogic.loggedInUpdatePass(request)

@api_view(['PUT'])
@permission_classes([sessionCustomAuthentication])
def editorResetPass(request):
    if request.method == 'PUT':
        return functionLogic.targetEmailPasswordresetToEmail(request)

@api_view(['PUT'])
@permission_classes([sessionCustomAuthentication])
def editorChangePass(request):
    if request.method == 'PUT':
        return functionLogic.targetEmailSetPassword(request)


@api_view(['GET'])
def testFunction(request):
    if request.method == 'GET':

        try:
            pass
            # SID = os.getenv('TWILIO_SID')
            # auth = os.getenv('TWILIO_AUTH')
            # client = Client(SID, auth)
            #
            # message = client.messages.create(
            #     body='Hi there',
            #     from_='+14754052778',
            #     to='+639672945681'
            # )
            # print(message.sid)
        except Exception as e:
            print(e)
            return Response({'error':'Internal Error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response(status=status.HTTP_200_OK)

@permission_classes([sessionCustomAuthentication])
@api_view(['GET'])
def textPeople(request):
    if request.method == 'GET':
        today = timezone.now().today()
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
            request.session['email'] = user.email
            request.session['role'] = user.role.role_name
            return Response({"message": "Login successful.","role": user.role.role_name}, status.HTTP_200_OK)
        else:
            return Response({'error':'Unauthorized'},status=status.HTTP_401_UNAUTHORIZED)

@permission_classes([sessionCustomAuthentication])
class LogoutPoint(APIView):
    def delete(self, request, format=None):
        try:
            request.session.delete()
            response = Response(status=status.HTTP_200_OK)
            return response
        except KeyError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([sessionCustomAuthentication])
def logoutAllUsers(request):
    if request.method == 'DELETE':
        getRole = roleClassify()
        strRole = getRole.roleReturn(request)
        if strRole == "Editor":
            return functionLogic.sessionTableClear(request)
        else:
            return Response({'message': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

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
        strRole = self.roleLookup.roleReturn(request)
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
        strRole = self.roleLookup.roleReturn(request)
        if strRole == "Editor" or strRole == "Admin":
            return self.create(request)
        else:
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)


    def put(self, request, category_id=None):
        strRole = self.roleLookup.roleReturn(request)
        if strRole == "Editor" or strRole == "Admin":
            return self.update(request, category_id)
        else:
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

    def delete(self, request, category_id=None):
        strRole = self.roleLookup.roleReturn(request)
        if strRole == "Editor":
            return self.destroy(request, category_id)
        else:
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)


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
        strRole = self.roleLookup.roleReturn(request)
        if strRole == "Editor" or strRole == "Admin":
            return self.update(request, item_code)
        else:
            return Response({'message':'Unauthorized'}, status=status.HTTP_200_OK)

    def get(self, request, item_code=None, filter=None):
        strRole = self.roleLookup.roleReturn(request)
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
        strRole = self.roleLookup.roleReturn(request)
        if strRole == "Editor" or strRole == "Admin":
            serializer = multipleItemInsertSerializer(data=request.data, many=True)
            if serializer.is_valid(raise_exception=False):
                self.perform_create(serializer)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

    def patch(self, request):
        strRole = self.roleLookup.roleReturn(request)
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
        strRole = self.roleLookup.roleReturn(request)
        if strRole == "Editor":
            return self.destroy(request, item_code)
        else:
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

class UsersClass(generics.GenericAPIView, mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, mixins.RetrieveModelMixin, mixins.ListModelMixin):
    permission_classes = [sessionCustomAuthentication]
    serializer_class = UserTableSerializer
    queryset = UserTable.objects.all()
    lookup_field = 'email'
    roleLookup = roleClassify()

    def get(self, request, email=None):
        strRole = self.roleLookup.roleReturn(request)
        if strRole == "Editor" or strRole == "Admin":
            if email:
                return self.retrieve(request)
            else:
                return self.list(request)
        else:
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

    def post(self, request):
        strRole = self.roleLookup.roleReturn(request)
        if strRole == "Editor" or strRole == "Admin":
            serializer = UserInsertTableSerializer(data=request.data, many=True)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

    def put(self, request, email=None):
        strRole = self.roleLookup.roleReturn(request)
        if strRole == "Editor":
            user = UserTable.objects.get(email=email)
            try:
                user.phone_number = request.data['phone_number']
            except:
                pass
            try:
                role = RoleTable.objects.get(role_id=request.data['role'])
                user.role = role
            except:
                pass
            user.save()
            return self.retrieve(request)
        return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

    def delete(self, request, email=None):
        strRole = self.roleLookup.roleReturn(request)
        if strRole == "Editor":
            if email:
                return self.destroy(request, email)
            else:
                data = request.data
                deletionCount = 0
                for select in data:
                    try:
                        userObj = UserTable.objects.get(email=select['email'])
                        userObj.delete()
                        deletionCount += 1
                    except:
                        pass
                return Response({'message': 'Accounts Deleted',
                                 'accounts_deleted': str(deletionCount)}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

class HistoryClass(generics.GenericAPIView, mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, mixins.RetrieveModelMixin, mixins.ListModelMixin):
    permission_classes = [sessionCustomAuthentication]
    serializer_class = HistorySerializer
    queryset = HistoryTable.objects.all()
    roleLookup = roleClassify()
    historyBack = historyLogic()
    lookup_field = 'history_id'
    lookup_url_kwarg = 'history_id'
    startdate_lookup_field = 'start_date'
    startdate_lookup_url_kwarg = 'start_date'
    enddate_lookup_field = 'end_date'
    endate_lookup_url_kwarg = 'end_date'
    lost_lookup_field = 'lost'
    lost_lookup_url_kwarg = 'lost'
    return_lookup_field = 'returnItems'
    return_lookup_url_kwarg = 'returnItems'
    clearLogs_lookup_field = 'clearLogs'
    clearLogs_lookup_url_kwarg = 'clearLogs'

    def get(self, request, history_id=None, start_date=None, end_date=None, returnItems=None):
        strRole = self.roleLookup.roleReturn(request)
        if strRole == "Admin" or strRole == "Editor":
            if history_id:
                return self.historyBack.historySearch(history_id, self.get_queryset())
            if start_date and end_date:
                return self.historyBack.historySearchDateRange(start_date, end_date)
            if returnItems:
                serializer = specialHistorySerializer(self.get_queryset().order_by('date_out').filter(date_out__isnull=True), many=True)
                return Response(serializer.data)
            else:
                serializer = specialHistorySerializer(self.get_queryset().order_by('date_out'), many=True)
                return Response(serializer.data)
        else:
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

    def put(self, request, history_id=None, lost=None, returnItems=None):
        strRole = self.roleLookup.roleReturn(request)
        if strRole == "Admin" or strRole == "Editor":
            if history_id:
                return self.update(request, history_id)
            if returnItems:
                return self.historyBack.returnItems(request)
            if lost:
                return self.historyBack.markItemasLost(request)
        else:
            return Response({'message': 'Unauthorized Access'}, status=status.HTTP_200_OK)

    def post(self, request):
        strRole = self.roleLookup.roleReturn(request)
        if strRole == "Editor" or strRole == "Admin":
            return self.historyBack.newBorrow(request)
        else:
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

    def delete(self, request, history_id=None, clearLogs=None):
        strRole = self.roleLookup.roleReturn(request)
        if strRole == "Editor":
            if history_id:
                return self.destroy(request, history_id)
            if clearLogs:
                HistoryTable.objects.all().delete()
                return Response({'message': 'history logs deleted'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

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
    clearLogs_lookup_field = 'clearLogs'
    clearLogs_lookup_url_kwarg = 'clearLogs'
    emailSearch_lookup_field = 'emailSearch'
    emailSearch_lookup_url_kwarg = 'emailSearch'


    def get(self, request, reservation_id=None, emailSearch=None):
        strRole = self.roleLookup.roleReturn(request)
        if strRole == "Editor" or strRole == "Admin":
            if reservation_id:
                queryset = self.get_queryset().filter(reservation_id=reservation_id)
                serializer = specialReservationSerializer(queryset, many=True)
                return Response(serializer.data)
            if emailSearch:
                queryset = self.get_queryset().filter(email=emailSearch)
                serializer = specialReservationSerializer(queryset, many=True)
                return Response(serializer.data)
            else:
                serializer = specialReservationSerializer(self.get_queryset(), many=True)
                return Response(serializer.data)
        else:
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

    def post(self, request):
        return self.perform_create(request)

    def put(self, request, reservation_id=None):
        strRole = self.roleLookup.roleReturn(request)
        if strRole == "Editor" or strRole == "Admin":
            return self.update(request, reservation_id)
        else:
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

    def delete(self, request, reservation_id=None):
        return self.destroy(request, reservation_id)

    def perform_create(self, request):
        today = timezone.now().today()
        data = request.data
        email = request.session['email']
        insertedData = 0
        for eachData in data:
            item_code = eachData['item_code']
            try:
                email = eachData['email']
            except:
                pass
            condition1 = InventoryTable.objects.filter(
                ~Q(item_code__in=ReservationTable.objects.filter(date_of_expiration__gte=today).filter(claim=0).values_list(
                    'item_code', flat=True)) & ~Q(item_code__in=HistoryTable.objects.filter(date_out__isnull=True).values_list('item_code', flat=True))).filter(item_code=item_code).filter(status="Available").select_related('category')
            condition2 = InventoryTable.objects.filter(status="Available").filter(item_code=item_code)
            if condition1.exists() and condition2.exists():
                user = UserTable.objects.get(email=email)
                item = InventoryTable.objects.get(item_code=item_code)
                reservation = ReservationTable.objects.create(
                    email=user,
                    item_code=item,
                    claim=0
                )
                reservation.save()
                insertedData += 1
            else:
                pass
        if insertedData > 0:
            return Response({'message': 'items reserved: ' + str(insertedData)}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'No item was reserved'}, status=status.HTTP_204_NO_CONTENT)

#special classes
class specificHistoryClass(generics.GenericAPIView):
    permission_classes = [sessionCustomAuthentication]
    serializer_class = specificUserHistorySerializer
    queryset = HistoryTable.objects.all()
    roleLookup = roleClassify()

    def post(self, request):
        email = None
        if settings.DEBUG is False:
            email = request.session['email']
        else:
            email = request.data['email']
        serializer = specificUserHistorySerializer(self.get_queryset().order_by('date_out').filter(email=email).filter(date_out__isnull=False), many=True)
        return Response(serializer.data)

    def getRole(self, request):
        try:
            lookUpRole = self.roleLookup.roleReturn(request)
            return lookUpRole
        except:
            return ""

class specificReservationClass(generics.GenericAPIView):
    permission_classes = [sessionCustomAuthentication]
    serializer_class = specificUserReservationSerializer
    queryset = ReservationTable.objects.all()
    roleLookup = roleClassify()

    def post(self, request):
        email = request.session['email']
        serializer = self.get_serializer(self.get_queryset().order_by('-date_of_expiration').filter(email=email), many=True)
        return Response(serializer.data)

class specificUserreservationsClass(generics.GenericAPIView):
    permission_classes = [sessionCustomAuthentication]
    serializer_class = ReservationSerializer
    reservationLogic = reservationLogic()
    roleLookup = roleClassify()

    def post(self, request):
        return self.reservationLogic.specificUserReservation(request)

class reservationTransfer(generics.GenericAPIView):
    permission_classes = [sessionCustomAuthentication]
    serializer_class = specificUserHistorySerializer
    reserveLogic = reservationLogic()
    roleLookup = roleClassify()

    def post(self, request):
        strRole = self.roleLookup.roleReturn(request)
        if strRole == "Editor" or strRole == "Admin":
            return self.reserveLogic.transferReservetoBorrow(request)
