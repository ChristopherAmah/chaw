from cart.models import Shopcart


def cartcount(request):
    count = Shopcart.objects.filter(user__username = request.user.username, paid= False)
    user1 = user__username = 1
    
    itemcount = 0

    for item in count:
        # itemcount += item.c_item
        itemcount += user1

    context = {
        'itemcount': itemcount,
    }

    return context