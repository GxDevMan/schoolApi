from django.conf import settings
from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.contrib.sessions.models import Session
from rest_framework import status
from rest_framework.response import Response
from django.db.models import Q
from userPortal.backends import roleClassify
from userPortal.models import ReservationTable, InventoryTable, HistoryTable, UserTable, CategoryTable
from userPortal.serializers import specialInventorySerializer, changePassSerializer, pendingReservationSerializer


def sessionTableClear():
    Session.objects.all().delete()
    return Response({'Message': 'All Users Logged out'}, status=status.HTTP_200_OK)

def returnItemsviewReserve(categoryId):
    today = timezone.now().today()
    query = None
    if categoryId:
        try:
            categoryObj = CategoryTable.objects.get(category_id=categoryId)
            query = InventoryTable.objects.filter(
                ~Q(item_code__in=ReservationTable.objects.filter(date_of_expiration__gte=today).filter(claim=0).values_list(
                    'item_code', flat=True)) &
                ~Q(item_code__in=HistoryTable.objects.filter(date_out__isnull=True).values_list('item_code',
                                                                                                flat=True))).filter(
                status="Available").filter(category=categoryObj).select_related('category')
        except:
            return Response({'error': 'category not found'}, status=status.HTTP_404_NOT_FOUND)

    else:
        query = InventoryTable.objects.filter(
            ~Q(item_code__in=ReservationTable.objects.filter(date_of_expiration__gte=today).filter(claim=0).values_list(
                'item_code', flat=True)) &
            ~Q(item_code__in=HistoryTable.objects.filter(date_out__isnull=True).values_list('item_code',
                                                                                            flat=True))).filter(
            status="Available").select_related('category')

    serializer = specialInventorySerializer(query, many=True)
    return Response(serializer.data)


def loggedInUpdatePass(request):
    try:
        sessionemail = None
        if settings.DEBUG:
            sessionemail = request.data['email']
        else:
            sessionemail = request.session['email']
        old_password = request.data['old_password']

        new_password = request.data['new_password']
        new_password2 = request.data['user_password']

        if new_password != new_password2:
            return Response({'message':'password does not match'}, status=status.HTTP_409_CONFLICT)

        selectedData = get_object_or_404(UserTable, email=sessionemail)
        user = authenticate(request, email=sessionemail, password=old_password)
        if user and new_password2 == old_password:
            return Response({'message': 'New password matches old password'}, status=status.HTTP_400_BAD_REQUEST)

        if user is not None:
            serializer = changePassSerializer(selectedData, request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'password successfully changed'})
        else:
            return Response({'error': 'password does not match the old password'}, status=status.HTTP_404_NOT_FOUND)
    except:
        return Response({'message': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

def targetEmailPasswordresetToEmail(request):
    try:
        getRole = roleClassify()
        strRole = getRole.roleReturn(request)
        if strRole == "Editor":
            selectedEmail = request.data['email']
            query = UserTable.objects.get(email=selectedEmail)
            query.user_password = query.email
            query.save()
            return Response({'message': 'User Password Reset to user email'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
    except:
        return Response({'message': 'Failed to reset Password'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def clearReserveTable(request):
    getRole = roleClassify()
    strRole = getRole.roleReturn(request)
    if strRole == "Editor":
        try:
            today = timezone.now().today()
            filteredData = ReservationTable.objects.filter(Q(claim=1) | Q(date_of_expiration__lt=today))
            filteredData.delete()
            return Response({'Message': 'Unecessarry reservations deleted'})
        except:
            return Response({'Message': 'Exception Occured'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response({'message': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

def getPendingreservation():
    try:
        today = timezone.now().today()
        filteredData = ReservationTable.objects.filter(claim=0).filter(date_of_expiration__gte=today).select_related(
            'item_code')
        serializer = pendingReservationSerializer(filteredData, many=True)
        return Response(serializer.data)
    except:
        return Response({'message': 'exception type'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def targetEmailSetPassword(request):
    try:
        getRole = roleClassify()
        strRole = getRole.roleReturn(request)
        if strRole == "Editor":
            selectedEmail = request.data['email']
            passwordInput = request.data['password']
            query = UserTable.objects.get(email=selectedEmail)
            query.user_password = passwordInput
            query.save()
            return Response({'message': 'password set'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
    except:
        return Response({'message': 'Failed to reset Password'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)