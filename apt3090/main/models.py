from django.db import models
from django.contrib.auth.models import User
from django.db import connection, models
import re


# Create your models here.
# customer
class Customer(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True,unique=True)
    email = models.CharField(max_length=200,  null=True)
    phone = models.CharField(max_length =200, null=True)
    date_created = models.DateTimeField(auto_now_add=True,  null=True)
    # AES ENCRYPTION PART
    credit_card_number_encrypted = models.CharField(max_length=200,  null=True)

    def _get_card(self):
        cursor = connection.cursor()
        cursor.execute("SELECT AES_DECRYPT(UNHEX(credit_card_number_encrypted), %s) as card_number FROM tablename WHERE id=%s",
                       ['settings.SECRET_KEY', self.id])
        return cursor.fetchone()[0]

    def _set_card(self, card_number_value):
        cursor = connection.cursor()
        cursor.execute("SELECT HEX(AES_ENCRYPT(%s, %s)) as card_number", [card_number_value, "settings.SECRET_KEY"])
        self.credit_card_number_encrypted = cursor.fetchone()[0]

    credit_card = property(_get_card, _set_card)

    cvv_encrypted = models.CharField(max_length=18,  null=True)
    expiry_month = models.CharField(max_length=3,  null=True)
    expiry_year = models.CharField(max_length=4,  null=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    CATEGORY = (
                    ('Sinks', 'Sinks'),
                    ('Pipes', 'Pipes'),
                    ('Toilets', 'Toilets'),
                )

    name=models.CharField(max_length=200, null=True)
    price=models.FloatField(max_length=200, null=True)
    category=models.CharField(max_length=200, null=True,choices=CATEGORY)
    description=models.CharField(max_length=200, null=True, blank=True)
    date_created=models.DateTimeField(auto_now_add=True,  null=True)
    image_url = models.CharField(max_length=200, null=True,default='https://upload.wikimedia.org/wikipedia/commons/8/89/Portrait_Placeholder.png' )
    stock_number = models.IntegerField(null=True, default=0)

    def __str__(self):
        return self.name

class Order(models.Model):
    STATUS =(
                ('Pending', 'Pending'),
                ('Cancelled', 'Cancelled'),
                ('Delivered', 'Delivered'),
            )
    customer = models.ForeignKey(Customer, null=True, on_delete = models.SET_NULL)
    product =models.ForeignKey(Product, null=True, on_delete = models.SET_NULL)
    status =models.CharField(max_length=200, null=True, choices=STATUS)
    date_created=models.DateTimeField(auto_now_add=True,  null=True)


    def __str__(self):
        return self.status


class Intern(models.Model):
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name
