import requests
import json
import uuid


from multiprocessing import context
from django.shortcuts import render,redirect, HttpResponse
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import EmailMessage
from django.conf import settings



from techbro.models import *
from dashboard.models import *
from cart.models import * #import all models from models.py file here
from techbro.forms import SignupForm
from dashboard.forms import ProfileUpdateForm

# Create your views here.
def index(request):
    #query the Database to pull objects out
    categories = Category.objects.all()[:6]
    specials = Dish.objects.filter(special=True)
    slide1 = Showcase.objects.get(pk=1)
    slide2 = Showcase.objects.get(pk=2)
    slide3 = Showcase.objects.get(pk=3)

    context = {
        'categories':categories,
        'specials':specials,
        'slide1':slide1,
        'slide2':slide2,
        'slide3':slide3,
    }
    
    return render(request, 'index.html', context)

def contactt(request):
    return render(request, 'contact.html')
   

def all_food(request):
    all_meals = Dish.objects.all()
    categories = Category.objects.all()
    specials = Dish.objects.filter(special=True)

    context = {
        'all_meals':all_meals,
        'categories':categories,
        'specials':specials,
    }
    return render(request, 'all_food.html', context)

def categories(request):
    categories = Category.objects.all()
    specials = Dish.objects.filter(special=True)

    context = {
        'categories':categories,
        'specials':specials,
    }
    return render(request, 'categories.html', context)


def single_category(request, id):
    specials = Dish.objects.filter(special=True)
    categories = Category.objects.all()
    single_category = Dish.objects.filter(category_id = id)
    cat_title = Category.objects.get(pk=id)

    context = {
        'specials':specials,
        'categories':categories,
        'category': single_category,
        'cat_title': cat_title,
    }
    return render(request, 'category.html', context)


def detail(request, id):
    specials = Dish.objects.filter(special=True)
    categories = Category.objects.all()
    detail = Dish.objects.get(pk=id)

    context = {
        'specials':specials,
        'categories':categories,
        'detail':detail,
    }
    return render(request, 'detail.html', context)

# authentication configuration
def signout(request):
    logout(request)
    messages.success(request, 'You have now signed out successfully' )
    return redirect('signin')

def signin(request):
    if request.method == "POST":
        myusername = request.POST['username']
        mypassword = request.POST['password']
        user = authenticate(request, username = myusername, password = mypassword)
        if user:
            login(request, user)
            messages.success(request, f'Welcome, {user.username}' )
            return redirect('index')
        else:
            messages.warning(request, 'Username/Password is incorrect')
            return redirect('signin')
    return render(request, 'signin.html')
 
def signup(request):
    # make a grt request to pull out and display the SignupForm 
    form = SignupForm() #instantiate the Signupform for a GET request
    if request.method == 'POST':
        phone = request.POST['phone']
        image = request.POST['image']
        form = SignupForm(request.POST) #instantiate the Signupform for a POST request
        if form.is_valid(): #test from our virus free, and declare valid
            form.save() #save incoming data
            userform = form.save()
            newuser = Profile(user = userform)
            newuser.first_name = userform.first_name
            newuser.last_name = userform.last_name
            newuser.email = userform.email
            newuser.phone = phone
            newuser.profile_pix = image
            newuser.save()
            messages.success(request, 'Signup successful!') #send success message to your user
            login(request, userform)
            return redirect('index') #redirect the user to any page of your choice
        else:
            messages.error(request, form.errors) #send out error message
            return redirect('signup') #if error occurs at signup attempt, keep user on signup page
            
    return render(request, 'signup.html')
# authentication configuration done

@login_required(login_url='signin')
# dashboard configuration
def profile(request):
    profile_data = Profile.objects.get(user__username = request.user.username)

    context = {
        'profile_data':profile_data
    }
    return render(request, 'dashboard.html', context)

@login_required(login_url='signin')
def profileupdate(request):
    profile_data = Profile.objects.get(user__username = request.user.username)
    form = ProfileUpdateForm(instance=request.user.profile)
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile Update successful')
            return redirect('profile')
        else:
            messages.error(request, form.errors)
            return redirect('profileupdate')
    context = {
        'form':form,
        'profile_data':profile_data,
    }
    return render(request, 'profileupdate.html', context)


@login_required(login_url='signin')
def passwordupdate(request):
    profile_data = Profile.objects.get(user__username = request.user.username)
    form = PasswordChangeForm(request.user)
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Password update successful')
            return redirect('profile')
        else:
            messages.error(request, form.errors)
            return redirect('passwordupdate')

    context = {
        'profile_data':profile_data,
        'form':form,
    }

    return render(request, 'profilepassword.html', context)
# dashboard configuration done


#shopcart
@login_required(login_url='signin')
def ordermeal(request):
    profile_data = Profile.objects.get(user__username = request.user.username)
    cart_no = profile_data.id
    if request.method == 'POST':
        quantityselected = int(request.POST['mealquantity'])
        meal = request.POST['mealid']
        mealselected = Dish.objects.get(pk=meal)
        cart = Shopcart.objects.filter(user__username= request.user.username, paid=False)
        if cart:
            basket = Shopcart.objects.filter(dish=mealselected.id, user__username= request.user.username, paid=False).first()
            if basket:
                basket.quantity += quantityselected
                basket.amount = basket.quantity * basket.c_price
                basket.save()
                messages.success(request, 'Your meal is being processed')
                return redirect('all_food')
            else:
                neworder = Shopcart()
                neworder.user = request.user
                neworder.dish = mealselected
                neworder.c_name = mealselected.name
                # neworder.c_item = 1
                neworder.quantity = quantityselected
                neworder.c_price = mealselected.price
                neworder.amount = mealselected.price * quantityselected
                neworder.cart_code = cart_no
                neworder.paid = False
                neworder.save()
                messages.success(request, 'Your meal is being processed')
                return redirect('all_food')
        else:
            newitem = Shopcart()
            newitem.user = request.user
            newitem.dish = mealselected
            newitem.c_name = mealselected.name
            # newitem.c_item = 1
            newitem.quantity = quantityselected
            newitem.c_price = mealselected.price
            newitem.amount = mealselected.price * quantityselected
            newitem.cart_code = cart_no
            newitem.paid = False
            newitem.save()
            messages.success(request, 'Your meal is being processed!.')
    return redirect('all_food')

@login_required(login_url='signin')
def mycart(request):
    profile = Profile.objects.get(user__username = request.user.username)
    shopcart = Shopcart.objects.filter(user__username = request.user.username, paid=False)

    subtotal = 0
    vat = 0
    total = 0

    for item in shopcart:
        subtotal += item.amount

    #7.5% of subtotal
    vat = 0.075 * subtotal

    total = vat + subtotal

    context = {
        'profile':profile,
        'shopcart':shopcart,
        'subtotal':subtotal,
        'vat':vat,
        'total':total,
    }
    return render(request, 'cart.html', context)

def deletemeal(request):
    if request.method == 'POST':
        meal = request.POST['dishid']
        deletedish = Shopcart.objects.get(pk=meal)
        deletedish.delete()
        messages.success(request, 'Meal item deleted successfully.')
    return redirect('mycart')

def clearcart(request):
    if request.method == 'POST':
        cleardish = Shopcart.objects.filter(user__username = request.user.username)
        cleardish.delete()
        messages.success(request, 'Cart cleared successfully.')
    return redirect('mycart')

# decrease cart item quantity
@login_required(login_url='signin')
def decrease(request):
    if request.method == 'POST':
        itemquantity = int(request.POST['decrease'])
        cartitem = request.POST['itemid']
        decreasecart = Shopcart.objects.get(pk= cartitem)
        decreasecart.quantity -= itemquantity
        decreasecart.amount = decreasecart.c_price * decreasecart.quantity
        decreasecart.save()
        messages.success(request, 'Quantity decreased.')
    return redirect('mycart')

    

# increase cart item quantity
@login_required(login_url='signin')
def increase(request):
    if request.method == 'POST':
        itemquantity = int(request.POST['increase'])
        cartitem = request.POST['itemid']
        increasecart = Shopcart.objects.get(pk= cartitem)
        increasecart.quantity += itemquantity
        increasecart.amount = increasecart.c_price * increasecart.quantity
        increasecart.save()
        messages.success(request, 'Quantity increased.')
    return redirect('mycart')

@login_required(login_url='signin')
def checkout(request):
    profile = Profile.objects.get(user__username = request.user.username)
    shopcart = Shopcart.objects.filter(user__username = request.user.username, paid=False)

    subtotal = 0
    vat = 0
    total = 0

    for item in shopcart:
        subtotal += item.amount

    #7.5% of subtotal
    vat = 0.075 * subtotal

    total = vat + subtotal

    context = {
        'profile':profile,
        'shopcart':shopcart,
        'subtotal':subtotal,
        'vat':vat,
        'total':total,
    }
    return render(request, 'checkout.html', context)
# shopcart done
# http://127.0.0.1:8000/completed

# 54.88.9.232
# payment
@login_required(login_url='signin')
def payment(request):
    if request.method == 'POST': #integrate API
        api_key = 'sk_test_378e7a9f7c1350b2370e142227e7a82a54b638f4'
        curl = 'https://api.paystack.co/transaction/initialize'
        cburl = 'http://54.88.9.232/completed'
        # cburl = 'http://127.0.0.1:8000/completed'
        ref_code = str(uuid.uuid4())
        user = User.objects.get(username = request.user.username)
        email = user.email
        profile = Profile.objects.get(user__username = request.user.username)
        cart_code = profile.id
        total = float(request.POST['total']) * 100
        fname = request.POST['first_name']
        lname = request.POST['last_name']
        phone = request.POST['phone']
        address = request.POST['address']
        city = request.POST['city']
        new_email = request.POST['email']


        headers = {'Authorization': f'Bearer {api_key}'} #pass in the test key
        data = {'reference': ref_code, 'amount': int(total), 'order_number': cart_code, 'email': email, 'callback_url': cburl, 'currency': 'NGN'}

        try: #make call to Paystack
            r = requests.post(curl, headers=headers, json=data)#pip install requests
        except Exception:
            messages.error(request, 'Network busy, refresh and try again.')
        else:
            transback = json.loads(r.text) #import json, import requests
            rurl = transback['data']['authorization_url']

            account = Payment()
            account.user = user
            account.first_name = fname
            account.last_name = lname
            account.phone = phone
            account.address = address
            account.city = city
            account.total = total/100
            account.cart_code = cart_code
            account.pay_code = ref_code
            account.paid = True
            account.save()

            email = EmailMessage(
                'Order confirmation',#message Tile
                f'Dear {fname}, your order is confirmed! \n your delivery is on the way. \n Thank you for your patronage.',#content
                settings.EMAIL_HOST_USER,#company email
                [new_email]#client email
            )

            email.fail_silently = True   
            email.send()     

            return redirect(rurl)
    return redirect('checkout')

def completed(request):
    profile_data = Profile.objects.get(user__username = request.user.username)
    cart = Shopcart.objects.filter(user__username = request.user.username, paid=False)

    for item in cart:
        item.paid = True
        item.save()

        stock = Dish.objects.get(pk = item.dish.id)
        stock.max -= item.quantity
        stock.save() 

    context = {
        'profile_data':profile_data,
    }
    return render(request, 'completed.html', context)