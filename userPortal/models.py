from django.db import models
from django.contrib.auth.hashers import PBKDF2PasswordHasher
#db
class CategoryTable(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=200)

    class Meta:
        managed = False
        db_table = 'category_table'

    def __str__(self):
        return self.category_name

class HistoryTable(models.Model):
    history_id = models.AutoField(primary_key=True)
    email = models.ForeignKey('UserTable', models.DO_NOTHING, db_column='email')
    item_code = models.ForeignKey('InventoryTable', models.DO_NOTHING, db_column='item_code')
    date_in = models.DateTimeField()
    date_out = models.DateTimeField(blank=True, null=True)
    due_date = models.DateField()
    notes = models.CharField(max_length=200)

    class Meta:
        managed = False
        db_table = 'history_table'

    def __str__(self):
        return str(self.item_code)

class InventoryTable(models.Model):
    item_code = models.AutoField(primary_key=True)
    category = models.ForeignKey(CategoryTable, models.DO_NOTHING)
    item_name = models.CharField(max_length=200)
    item_condition = models.CharField(max_length=100)
    status = models.CharField(max_length=100)

    def __str__(self):
        formatString = "{itemCode} : {itemName}"
        return formatString.format(itemCode=self.item_code, itemName=self.item_name)

    class Meta:
        managed = False
        db_table = 'inventory_table'


class ReservationTable(models.Model):
    reservation_id = models.AutoField(primary_key=True)
    email = models.ForeignKey('UserTable', models.DO_NOTHING, db_column='email')
    item_code = models.ForeignKey(InventoryTable, models.DO_NOTHING, db_column='item_code')
    data_of_reservation = models.DateField()
    date_of_expiration = models.DateField()
    claim = models.IntegerField()

    def __str__(self):
        stringZ = "{email} : {firstName} {lastName}"
        return stringZ.format(email=self.email.email,
                              firstName=self.email.first_name,
                              lastName=self.email.last_name)

    class Meta:
        managed = False
        db_table = 'reservation_table'

class RoleTable(models.Model):
    role_id = models.AutoField(primary_key=True)
    role_name = models.CharField(max_length=200)

    def __str__(self):
        return self.role_name;

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

#special models

