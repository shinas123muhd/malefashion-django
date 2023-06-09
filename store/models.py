from django.db import models
from django.urls import reverse
from category.models import Category
from django.utils.text import slugify

# Create your models here.


class Product(models.Model):
    product_name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(max_length=250, blank=True)
    price = models.IntegerField()
    image = models.ImageField(upload_to="photos/products")
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def get_url(self):
        return reverse("product_details", args=[self.category.slug, self.slug])

    def __str__(self):
        return self.product_name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.product_name)
        super().save(*args, **kwargs)

    def discount_price(self):
        active_offers = Offer.objects.filter(product = self,is_active=True)
        if active_offers.exists():
            
            
            max_discount = active_offers.aggregate(models.Max('discount'))['discount__max']
            discounted_price = self.price - (self.price * (max_discount / 100))
            return discounted_price
        return self.price


class VariationManager(models.Manager):
    def sizes(self):
        return super(VariationManager, self).filter(
            variation_category="size", is_active=True
        )


variation_category_choice = (("size", "size"),)


class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation_category = models.CharField(
        max_length=100, choices=variation_category_choice
    )
    variation_value = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now=True)

    objects = VariationManager()

    def __str__(self):
        return self.variation_value
    
class Offer(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    discount = models.DecimalField(max_digits=5,decimal_places=2)
