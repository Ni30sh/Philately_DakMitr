from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Product(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='products/')
    price = models.DecimalField(max_digits=10, decimal_places=2)

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    token_number = models.PositiveIntegerField()
    address = models.TextField()
    pincode = models.CharField(max_length=6)
    ordered_at = models.DateTimeField(auto_now_add=True) 

class Stamp(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='stamps/')
    description = models.TextField()
    year = models.IntegerField()
    date_added = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

class Album(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    stamps = models.ManyToManyField(Stamp, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Album"
    
class Contact(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    problem = models.TextField()
    email_or_phone = models.CharField(max_length=100)
    date_submitted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.username}"
    
class Payment(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    stamp_type = models.CharField(max_length=100)
    razorpay_order_id = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)