from rest_framework import serializers
from .models import UserTable, \
    InventoryTable, \
    RoleTable, \
    ReservationTable, \
    CategoryTable, \
    HistoryTable

#1 is to 1
class UserTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserTable
        fields = ['email','role', 'phone_number', 'first_name', 'last_name']

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
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryTable
        fields = '__all__'

class HistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoryTable
        fields = '__all__'

#special serializers