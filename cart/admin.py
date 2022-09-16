from django.contrib import admin
from .models import Shopcart,Payment
# Register your models here.


@admin.register(Shopcart)
class ShopcartAdmin(admin.ModelAdmin):
    list_display = ['user','dish','c_name','quantity','c_price','amount','cart_code','paid','c_date']
    readonly_fields = ['user','dish','c_name','quantity','c_price','amount','cart_code','paid']

@admin.register(Payment)
class Payment(admin.ModelAdmin):
    list_display = ['user','first_name','last_name','total','cart_code','phone','address','city','pay_code','paid','pay_date','admin_note','admin_update']
    readonly_fields = ['user','first_name','last_name','total','cart_code','phone','address','city','pay_code','paid','pay_date']