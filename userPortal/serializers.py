from django.db.models import Q
from rest_framework import serializers
from .models import UserTable, \
    InventoryTable, \
    RoleTable, \
    ReservationTable, \
    CategoryTable, \
    HistoryTable

#chain serializer
class ReservationHistoryExtSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryTable
        fields = ['item_code','category','item_name']
        depth = 1

class pendingExtReservation(serializers.ModelSerializer):
    class Meta:
        model = InventoryTable
        fields = ['item_code','item_name']

class HistoryReportExtUserTable(serializers.ModelSerializer):
    class Meta:
        model = UserTable
        fields = ['email','first_name','last_name']

#1 is to 1
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryTable
        fields = '__all__'

class UserTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserTable
        fields = '__all__'

class InventoryTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryTable
        fields = '__all__'

class RoleTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoleTable
        fields = '__all__'

class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReservationTable
        fields = ['email','item_code','data_of_reservation','date_of_expiration','claim']

class HistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoryTable
        fields = '__all__'


#special serializers
class specialInventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryTable
        fields = '__all__'
        depth = 1

class specialHistorySerializer(serializers.ModelSerializer):
    item_code = ReservationHistoryExtSerializer()
    email = HistoryReportExtUserTable()
    class Meta:
        model = HistoryTable
        fields = '__all__'

class specialReservationSerializer(serializers.ModelSerializer):
    item_code = ReservationHistoryExtSerializer()
    class Meta:
        model = ReservationTable
        fields = '__all__'

class specialInsertReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReservationTable
        fields = ['email','item_code','claim']

class specialInsertHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoryTable
        fields = ['email','item_code','due_date','notes']

class numberOnlyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserTable
        fields = ['email','phone_number']

class itemNameOnlySerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryTable
        fields = ['item_name']

class textPeopleFindSerializer(serializers.ModelSerializer):
    email = numberOnlyUserSerializer()
    item_code = itemNameOnlySerializer()
    class Meta:
        model = HistoryTable
        fields = ['email', 'item_code','due_date']

class specialHistoryReportSerializer(serializers.ModelSerializer):
    item_code = ReservationHistoryExtSerializer()
    email = HistoryReportExtUserTable()
    class Meta:
        model = HistoryTable
        fields = '__all__'

class multipleItemInsertSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryTable
        fields = ['category','item_name','item_condition','status']

class multipleItemUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryTable
        fields = ['item_code','category','item_name','item_condition','status']

class pendingReservationSerializer(serializers.ModelSerializer):
    item_code = pendingExtReservation()
    class Meta:
        model = ReservationTable
        fields = ['reservation_id','item_code','date_of_expiration']


class changePassSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserTable
        fields = ['user_password']