from django.utils import timezone

from django.db import models
from django.contrib.auth.hashers import PBKDF2PasswordHasher
#db

class RoleTable(models.Model):
    role_id = models.AutoField(primary_key=True)
    role_name = models.CharField(max_length=200)

    def __str__(self):
        return self.role_name

    class Meta:
        managed = False
        db_table = 'role_table'

class UserTable(models.Model):
    email = models.CharField(primary_key=True, max_length=200)
    role = models.ForeignKey(RoleTable, models.DO_NOTHING)
    phone_number = models.BigIntegerField()
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    user_password = models.CharField(max_length=1000)

    def save(self, *args, **kwargs):
        if self.user_password:
            self.user_password = PBKDF2PasswordHasher().encode(self.user_password, PBKDF2PasswordHasher().salt())
        super().save(*args, **kwargs)


    def __str__(self):
        stringFormat = "{email} : {firstName} {lastName} : {role}"
        return stringFormat.format(email=self.email,
                                   firstName=self.first_name,
                                   lastName=self.last_name,
                                   role=self.role.role_name)

    class Meta:
        managed = False
        db_table = 'user_table'

class CategoryTable(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=200)

    class Meta:
        managed = False
        db_table = 'category_table'

    def __str__(self):
        return self.category_name

class InventoryTable(models.Model):
    item_code = models.AutoField(primary_key=True)
    category = models.ForeignKey(CategoryTable, on_delete=models.CASCADE,db_column='category_id')
    item_name = models.CharField(max_length=200)
    item_condition = models.CharField(max_length=100)
    status = models.CharField(max_length=100)

    def __str__(self):
        formatString = "{itemCode} : {itemName} : {statusItem} : {itemCond}"
        return formatString.format(itemCode=self.item_code, itemName=self.item_name, statusItem=self.status, itemCond=self.item_condition)

    class Meta:
        managed = False
        db_table = 'inventory_table'

class ReservationTable(models.Model):
    reservation_id = models.AutoField(primary_key=True)
    email = models.ForeignKey('UserTable', on_delete=models.CASCADE, db_column='email')
    item_code = models.ForeignKey(InventoryTable, on_delete=models.CASCADE, db_column='item_code')
    data_of_reservation = models.DateField()
    date_of_expiration = models.DateField()
    claim = models.IntegerField()

    def save(self,  *args, **kwargs):
        if not self.data_of_reservation:
            today = timezone.now().today()
            today_str = today.strftime('%Y-%m-%d')
            self.data_of_reservation = today_str
        if not self.date_of_expiration:
            today = timezone.now().today()
            today_str = today.strftime('%Y-%m-%d')
            self.date_of_expiration = today_str
        super().save(*args, **kwargs)

    def __str__(self):
        stringZ = "{item} : {email} : {name} : Expiration - {datetime}"
        return stringZ.format(item=self.item_code.item_name, email=self.email.email, name=(self.email.first_name + " " + self.email.last_name), datetime=self.date_of_expiration)

    class Meta:
        managed = False
        db_table = 'reservation_table'

class HistoryTable(models.Model):
    history_id = models.AutoField(primary_key=True)
    email = models.ForeignKey('UserTable', db_column='email', on_delete=models.CASCADE)
    item_code = models.ForeignKey('InventoryTable', on_delete=models.CASCADE, db_column='item_code')
    date_in = models.DateTimeField()
    date_out = models.DateTimeField(blank=True, null=True)
    due_date = models.DateField()
    notes = models.CharField(max_length=200)

    class Meta:
        managed = False
        db_table = 'history_table'

    def save(self, *args, **kwargs):
        if not self.due_date:
            today = timezone.now().today()
            self.due_date = today
        if not self.date_in:
            today = timezone.now().today()
            self.date_in = today
        if not self.due_date:
            today = timezone.now().today()
            self.due_date = today
        if not self.notes:
            self.notes = "N/A"
        super().save(*args, **kwargs)


    def __str__(self):
        formatString = "{historyId} : {item} : {email} : {name} : {datetime}"
        return formatString.format(historyId=self.history_id, item=self.item_code.item_name, email=self.email.email, name=(self.email.first_name + " " + self.email.last_name), datetime=self.date_out)


