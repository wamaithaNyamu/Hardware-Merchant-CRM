from django.db import models

# Create your models here.
# customer
class Customer(models.Model):
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200,  null=True)
    phone = models.CharField(max_length =200, null=True)
    date_created = models.DateTimeField(auto_now_add=True,  null=True)
    
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
    description=models.CharField(max_length=200, null=True)
    date_created=models.DateTimeField(auto_now_add=True,  null=True)

    def __str__(self):
        return self.name

class Order(models.Model):
    STATUS =(
                ('Pending', 'Pending'),
                ('Cancelled', 'Cancelled'),
                ('Delivered', 'Delivered'),
            )
    #customer =
    #product =
    status =models.CharField(max_length=200, null=True, choices=STATUS)
    date_created=models.DateTimeField(auto_now_add=True,  null=True)


    def __str__(self):
        return self.status
