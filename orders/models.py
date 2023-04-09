from django.db import models
from accounts.models import Account
from store.models import Product

# Create your models here.
class Payment(models.Model):
    user = models.ForeignKey(Account,on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=100)
    payment_method = models.CharField(max_length=100)
    amount_paid = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.payment_id
    
class Order(models.Model):

    STATUS = (
        ('New','New'),
        ('Accepted','Accepted'),
        ('Completed','Completed'),
        ('Cancelled','Cancelled'),
    )
    user = models.ForeignKey(Account,on_delete=models.SET_NULL,null=True)
    payment = models.ForeignKey(Payment,on_delete=models.SET_NULL,blank=True,null=True)
    order_number = models.CharField(max_length=20)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    Phone = models.CharField(max_length=20)
    email = models.EmailField(max_length=20)
    address_line_1 = models.CharField(max_length=20)
    address_line_2 = models.CharField(max_length=20,blank=True)
    state = models.CharField(max_length=20)
    city = models.CharField(max_length=20)
    order_total = models.FloatField()
    tax = models.FloatField()
    status = models.CharField(max_length=10,choices=STATUS,default='new')
    ip = models.CharField(blank=True,max_length=20)
    is_ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.first_name

class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.CharField(max_length=10)
    quantity = models.IntegerField()
    product_price = models.FloatField()
    ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.product_name
