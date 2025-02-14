from django.contrib import admin

# Register your models here.
from .models import Order, Item
admin.site.register(Order)
admin.site.register(Item)