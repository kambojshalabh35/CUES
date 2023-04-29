from django.db import models
from django.contrib.auth.models import auth, User


class Seller(models.Model):
    user_linked = models.OneToOneField(User, on_delete=models.CASCADE)
    shop_name = models.CharField(max_length=75)
    contact_no = models.IntegerField()
    upi_id = models.CharField(max_length=50)

    def __str__(self):
        return self.shop_name
