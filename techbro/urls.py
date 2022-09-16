from django.urls import path
from .views import *


urlpatterns = [
    path('', index, name='index'),
    path('contact', contactt, name='contact'),
    path('all_food', all_food, name='all_food'),
    path('categories', categories, name='categories'),
    path('category/<str:id>', single_category, name='category'),
    path('detail/<str:id>', detail, name='detail'),
    path('signout', signout, name='signout'),
    path('signin', signin, name='signin'),
    path('signup', signup, name='signup'),
    path('profile', profile, name='profile'),
    path('profileupdate', profileupdate, name='profileupdate'),
    path('passwordupdate', passwordupdate, name='passwordupdate'),
    path('ordermeal', ordermeal, name='ordermeal'),
    path('mycart', mycart, name='mycart'),
    path('deletemeal', deletemeal, name='deletemeal'),
    path('clearcart', clearcart, name='clearcart'),
    path('decrease', decrease, name='decrease'),
    path('increase', increase, name='increase'),
    path('checkout', checkout, name='checkout'),
    path('payment', payment, name='payment'),
    path('completed', completed, name='completed'),
]