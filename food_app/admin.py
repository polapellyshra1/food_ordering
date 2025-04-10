
# Register your models here.
from django.contrib import admin
from .models import FoodItem, Order

admin.site.register(FoodItem)
admin.site.register(Order)
