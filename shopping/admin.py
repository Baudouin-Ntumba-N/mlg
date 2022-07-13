from django.contrib import admin
from .models import Order, OrderAdmin, Cart


# Register your models here.

admin.site.register(Order, OrderAdmin)
admin.site.register(Cart)