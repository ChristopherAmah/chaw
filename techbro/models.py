from email.policy import default
from pyexpat import model
from unicodedata import category
from django.db import models

# Create your models here.
class Category(models.Model):
    cat_name = models.CharField(max_length=50)
    cat_image = models.ImageField(upload_to='category')
    

    def __str__(self):
        return self.cat_name

    class Meta:
        db_table = 'category'
        managed = True
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Dish(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    breakfast = models.BooleanField(default=False)
    lunch = models.BooleanField(default=False)
    dinner = models.BooleanField(default=False)
    appetizer = models.BooleanField(default=False)
    dessert = models.BooleanField(default=False)
    drink = models.BooleanField(default=False)
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='food', default='pix.png', blank=True, null=True)
    price = models.IntegerField()
    min = models.IntegerField()
    max = models.IntegerField()
    special = models.BooleanField(default=False)
    in_stock = models.BooleanField()
    description = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'dish'
        managed = True
        verbose_name = 'Dish'
        verbose_name_plural = 'Dishes'


class Showcase(models.Model):
    show_name = models.CharField(max_length=50)
    show_txt = models.CharField(max_length=250)
    show_img = models.ImageField(upload_to='showcase', default='show.jpg')

    def __str__(self):
        return self.show_name
    
    class Meta:
        db_table = 'showcase'
        managed = True
        verbose_name = 'Showcase'
        verbose_name_plural = 'Showcases'

