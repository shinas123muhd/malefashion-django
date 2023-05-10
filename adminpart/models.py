from django.db import models

# Create your models here.
class Coupon(models.Model):
    coupon_code = models.CharField(max_length=10,null=False)
    min_amount = models.CharField(max_length=10,null=True)
    active_date = models.DateField(null=True)
    expire_date = models.DateField(null=True)
    discount_amount = models.CharField(max_length=10,default=100)
