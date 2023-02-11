from django.urls import path
from .views import viewUsers, viewItems, returnListofRoles, roles, CategoryClass
from .views import testFunction
from .views import reservationsClass, RoleClass, InventoryClass, HistoryClass, LoginPoint, LogoutPoint
urlpatterns = [
    path('userList/', viewUsers),
    path('inventoryList/', viewItems),
    path('roleList/', roles),

    path('reservation/<int:reservation_id>', reservationsClass.as_view()),
    path('reservation/', reservationsClass.as_view()),

    path('roles/<int:role_id>', RoleClass.as_view()),
    path('roles/', RoleClass.as_view()),

    path('category/<int:category_id>', CategoryClass.as_view()),
    path('category/', CategoryClass.as_view()),

    path('inventory/<int:item_code>', InventoryClass.as_view()),
    path('inventory/', InventoryClass.as_view()),

    path('history/<int:history_id>', HistoryClass.as_view()),
    path('history/',HistoryClass.as_view()),

    path('login/', LoginPoint.as_view()),

    path('logout/', LogoutPoint.as_view()),

    path('testing/', testFunction)
]