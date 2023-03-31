from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from userPortal.models import ReservationTable, UserTable, InventoryTable, HistoryTable
from django.db.models import Q
from django.conf import settings
class reservationLogic:
    #post Reservation Transfer
    def transferReservetoBorrow(self, request):
        data = request.data
        for eachData in data:
            today = timezone.now().today()
            today_str = today.strftime('%Y-%m-%d')

            reservationId = eachData['reservation_id']
            selectedReserve = ReservationTable.objects.filter(reservation_id=reservationId).filter(claim=False).filter(
                date_of_expiration__gte=today_str).first()
            notes = None
            try:
                notes = eachData['notes']
            except:
                pass
            try:
                user = UserTable.objects.get(email=selectedReserve.email.email)
                item = InventoryTable.objects.get(item_code=selectedReserve.item_code.item_code)
            except:
                return Response({'message': 'Reservation not found'},  status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            if user is not None and item is not None and selectedReserve is not None:
                history = HistoryTable.objects.create(
                    email=user,
                    item_code=item,
                    notes=notes,
                )
                selectedReserve.claim = True
                selectedReserve.delete()
                history.save()
        return Response({'message':'transfer complete'}, status=status.HTTP_200_OK)

    #specificUserreservation class post
    def specificUserReservation(self, request):
        data = request.data
        email = None
        if settings.DEBUG is False:
            email = request.session['email']

        itemsCount = 0
        for eachData in data:
            if settings.DEBUG:
                email = eachData['email']

            item_code = eachData['item_code']
            user = UserTable.objects.get(email=email)
            item = InventoryTable.objects.get(item_code=item_code)
            if self.performCheck(item_code):
                reserve = ReservationTable.objects.create(
                    email=user,
                    item_code=item,
                    claim=0,
                )
                reserve.save()
                itemsCount += 1
        if itemsCount > 0:
            return Response({'message': 'items successfully reserved: ' + str(itemsCount)}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'No item reserved'}, status=status.HTTP_204_NO_CONTENT)

    def performCheck(self, item_code):
        today = timezone.now().today()
        condition1 = InventoryTable.objects.filter(
            ~Q(item_code__in=ReservationTable.objects.filter(date_of_expiration__gte=today).filter(claim=0).values_list(
                'item_code', flat=True)) & ~Q(item_code__in=HistoryTable.objects.filter(date_out__isnull=True).values_list('item_code',flat=True))).filter(
            item_code=item_code).filter(status="Available").select_related('category')
        condition2 = InventoryTable.objects.filter(status="Available").filter(item_code=item_code)
        decision = condition1.exists() and condition2.exists()
        return decision