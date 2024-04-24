from django.contrib import admin
from .models import Discount,DiscountUserProfile,PayMentLog
# Register your models here.



admin.site.register(Discount)
admin.site.register(DiscountUserProfile)
admin.site.register(PayMentLog)