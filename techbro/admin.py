from django.contrib import admin
from .models import Category, Dish, Showcase
# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id','cat_name','cat_image']
    list_editable = ['cat_name','cat_image']


@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = ['id','category_id','category','name', 'image','special','breakfast','lunch','dinner','drink','appetizer','dessert','price','min','max','in_stock']
    list_editable = ['special']


@admin.register(Showcase)
class ShowcaseAdmin(admin.ModelAdmin):
    list_display = ['id','show_name','show_txt','show_img']
    



