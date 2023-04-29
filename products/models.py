from django.db import models
from adminAndSellers.models import Seller
from django.contrib.auth.models import User

# Create your models here.
class Product(models.Model):
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    seller_linked_user = models.TextField(blank=True, null=True)
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=55)
    description = models.TextField(blank=True, null=True)
    tag = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    added_date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='uploads/', blank=True, null=True) 
    noofsales = models.BooleanField(default=False)

    def __str__(self):
        return str(self.title)+" - "+str(self.seller.shop_name)

class Order(models.Model):
    orderNumber = models.AutoField(primary_key=True)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=55)
    title = models.CharField(max_length=50)
    contactNumber = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.TextField(blank=True, null=True)
    delivery_status = models.TextField(blank=True, null=True)
    order_time = models.DateTimeField(auto_now_add=True)
