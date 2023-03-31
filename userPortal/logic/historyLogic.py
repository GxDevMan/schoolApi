from datetime import timedelta
from django.db.models import Q
from django.utils import timezone
from rest_framework import status
from userPortal.models import HistoryTable, UserTable, InventoryTable
from userPortal.serializers import specialHistorySerializer, specialHistoryReportSerializer
from rest_framework.response import Response
from ..backends import convertDate

class historyLogic:
    dateConversion = convertDate()
    #get Logic
    def historySearch(self, history_id, queryset):
        queryset = queryset.filter(history_id=history_id)
        serializer = specialHistorySerializer(queryset, many=True)
        return Response(serializer.data)

    def historySearchDateRange(self, start_date, end_date):
        startingDate = self.dateConversion.dateFormattoYYMMDD(start_date)
        endingDate = self.dateConversion.dateFormattoYYMMDD(end_date)

        filteredData = HistoryTable.objects.filter(date_out__isnull=False).filter(
            date_out__range=(startingDate, endingDate + timedelta(days=1))).select_related(
            'item_code__category').select_related(
            'email')
        serializer = specialHistoryReportSerializer(filteredData, many=True)
        return Response(serializer.data)

    #post
    def newBorrow(self, request):
        data = request.data
        count = 0
        for eachData in data:
            email = eachData['email']
            if not email:
                email = request.session['email']
            item_code = eachData['item_code']

            date_in = None
            try:
                date_in = eachData['date_in']
            except:
                pass

            date_out = None
            try:
                date_out = eachData['date_out']
            except:
                pass

            due_date = None
            try:
                due_date = eachData['due_date']
            except:
                pass

            notes = None
            try:
                notes = eachData['notes']
            except:
                pass
            user = UserTable.objects.get(email=email)
            item = InventoryTable.objects.get(item_code=item_code)

            if self.performCheck(item_code):
                HistoryTable.objects.create(
                    email=user,
                    item_code=item,
                    date_in=date_in,
                    date_out=date_out,
                    due_date=due_date,
                    notes=notes
                )
                count += 1
        return Response({'Inserted_data': count}, status=status.HTTP_200_OK)

    def performCheck(self, item_code):
        condition1 = InventoryTable.objects.filter(
            ~Q(item_code__in=HistoryTable.objects.filter(date_out__isnull=True).values_list('item_code', flat=True))).filter(item_code=item_code).filter(status="Available").select_related('category')
        condition2 = InventoryTable.objects.filter(status="Available").filter(item_code=item_code)
        decision = condition1.exists() and condition2.exists()
        return decision

    #put
    def returnItems(self, request):
        data = request.data
        itemsReturned = 0
        for eachData in data:
            try:
                today = timezone.now().today()
                selectedHistory = HistoryTable.objects.get(history_id=eachData['history_id'])
                if selectedHistory.date_out is None:
                    note = None
                    try:
                        note = eachData['notes']
                    except:
                        pass
                    selectedHistory.date_out = today
                    selectedHistory.notes = note
                    itemsReturned += 1
                    selectedHistory.save()
            except:
                pass
        return Response({'message': 'Items returned, items now Available','items returned': itemsReturned}, status=status.HTTP_200_OK)

    def markItemasLost(self, request):
        data = request.data
        itemLostcount = 0
        for eachData in data:
            try:
                today = timezone.now().today()
                selectedHistory = HistoryTable.objects.get(history_id=eachData['history_id'])
                selectedHistory.notes = "Lost"
                selectedHistory.date_out = today

                selectedItem = InventoryTable.objects.get(item_code=selectedHistory.item_code.item_code)
                selectedItem.item_condition = "Lost"

                selectedItem.save()
                selectedHistory.save()
                itemLostcount += 1
            except:
                pass
        return Response({'message': 'Item/s marked as lost, items now unavailble','items lost': itemLostcount}, status=status.HTTP_200_OK)


