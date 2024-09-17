from django.contrib import admin
from .models import Product, Order
from .models import Stamp, Album,Contact,Payment

admin.site.register(Product)
admin.site.register(Order)
# Register your models here.


admin.site.register(Stamp)
admin.site.register(Album)
admin.site.register(Contact)
admin.site.register(Payment)