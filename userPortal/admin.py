from django.contrib import admin
from .models import UserTable, HistoryTable, CategoryTable, InventoryTable, ReservationTable, RoleTable

# Register your models here.
admin.site.register(UserTable)
admin.site.register(HistoryTable)
admin.site.register(CategoryTable)
admin.site.register(InventoryTable)
admin.site.register(RoleTable)
admin.site.register(ReservationTable)