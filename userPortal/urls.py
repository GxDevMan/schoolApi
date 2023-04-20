from django.urls import path
from .views import CategoryClass
from .views import testFunction
from .views import reservationsClass, InventoryClass, HistoryClass, LoginPoint, LogoutPoint, RoleClass, UsersClass
from .views import viewItemsthatCanBeReserved, pendingReservation, specificUserreservationsClass
from .views import logoutAllUsers, clearAllreservations, countStatus, textPeople, specificReservationClass
from .views import editorResetPass, editorChangePass, specificHistoryClass, reservationTransfer, updatePass
urlpatterns = [
    path('userChangePassword/', updatePass),
    path('editorResetPassword/', editorResetPass),
    path('editorChangePassword/', editorChangePass),

    path('reservation/<int:reservation_id>', reservationsClass.as_view()),
    path('reservation/', reservationsClass.as_view()),
    path('reservation/<str:emailSearch>', reservationsClass.as_view()),
    path('confirmReservation/', reservationTransfer.as_view()),
    path('pendingReservations/', pendingReservation),
    path('clearReservations/', clearAllreservations),
    path('specificReservations/', specificReservationClass.as_view()),
    path('specificUserInsertReservations/', specificUserreservationsClass.as_view()),

    path('textDueItems/', textPeople),

    path('roles/', RoleClass.as_view()),

    path('category/<int:category_id>', CategoryClass.as_view()),
    path('category/', CategoryClass.as_view()),

    path('inventory/<int:item_code>', InventoryClass.as_view()),
    path('inventory/<str:filter>', InventoryClass.as_view()),
    path('inventory/categoryFilter/<int:categoryId>', InventoryClass.as_view()),
    path('inventory/bothFilter/<int:categoryId>/<str:filter>', InventoryClass.as_view()),
    path('inventory/', InventoryClass.as_view()),
    path('statuscount/', countStatus.as_view()),

    path('itemsView/', viewItemsthatCanBeReserved),
    path('itemsView/categoryFilter/<int:categoryId>/', viewItemsthatCanBeReserved),

    path('user/<str:email>', UsersClass.as_view()),
    path('user/', UsersClass.as_view()),

    path('history/<int:history_id>', HistoryClass.as_view()),
    path('history/returnItems/<str:returnItems>', HistoryClass.as_view()),
    path('history/lost/<str:lost>', HistoryClass.as_view()),
    path('history/withRange/<str:start_date>/<str:end_date>', HistoryClass.as_view()),
    path('history/clearLogs/<str:clearLogs>', HistoryClass.as_view()),
    path('history/',HistoryClass.as_view()),

    path('userHistory/', specificHistoryClass.as_view()),

    path('login/', LoginPoint.as_view()),
    path('logout/', LogoutPoint.as_view()),
    path('logoutAllUsers/', logoutAllUsers),
    path('changePass/', updatePass),

    path('testing/', testFunction)
]