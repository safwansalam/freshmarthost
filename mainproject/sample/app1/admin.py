from django.contrib import admin
# from django.contrib.auth.models import User

from .models import *
admin.site.register([user_register,product,subscriptionPlan,Booking,category,cart,Wishlist,Contact])

# Register your models here.
