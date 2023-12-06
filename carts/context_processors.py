from .models import Cart, CartItem
from .views import _cart_id

# Context processors in Django are functions that add data to the context of every rendered template


def counter(request):
    cart_count = 0
    if 'admin' in request.path:
        return {}
# By returning an empty dictionary here, the context processor essentially does nothing in the case where the user is accessing the Django admin interface.
    else:
        try:
            cart = Cart.objects.filter(cart_id=_cart_id(request))
            if request.user.is_authenticated:
                cart_items = CartItem.objects.all().filter(user=request.user)
            else:
                cart_items = CartItem.objects.all().filter(cart=cart[:1])
                # ? I need only 1 result
                # ? ==> This is done to avoid potential issues if there are multiple carts associated with the user.
            for cart_item in cart_items:
                cart_count += cart_item.quantity
        except Cart.DoesNotExist:
            cart_count = 0
    return dict(cart_count=cart_count)
#: Returns a dictionary containing the cart_count variable.
# This will be added to the context of every template,
# making cart_count accessible in the templates.


'''
The reason for excluding the admin interface from the context processor might be to avoid 
unnecessary calculations or queries related to the shopping cart when a user is navigating 
the admin pages. The admin interface is typically used by site administrators and doesn't need 
information about the user's shopping cart. 
Therefore, this check optimizes the context processor to skip unnecessary processing
when dealing with admin-related requests.

'''
