from django.shortcuts import render, redirect, get_object_or_404
from .models import Cart, CartItem
from store.models import Product, Variation
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import requests
# ? _ : private function
# ? Add '_' in front of the name, it means that it's private function.
# ? _cart_id : private function


def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def add_cart(request, product_id):
    current_user = request.user
    product = Product.objects.get(id=product_id)  # Get the product
    product_variation = []
    # ? [product_variation = []]For making a list of variations. I added after try 'product_variation.append(variation)'

    if request.method == 'POST':
        # color = request.POST['color']
        # size = request.POST['size']
        for item in request.POST:
            key = item
            value = request.POST[key]
            try:
                variation = Variation.objects.get(product=product,
                                                  variation_category__iexact=key,  variation_value__iexact=value)
                product_variation.append(variation)
            except:
                # except Variation.DoesNotExist:
                pass

#! If the user is authenticated,
    if current_user.is_authenticated:
        # ? [product_variation = []]For making a list of variations. I added after try 'product_variation.append(variation)'
        # product_variation = []
        # if request.method == 'POST':
        #     # color = request.POST['color']
        #     # size = request.POST['size']
        #     for item in request.POST:
        #         key = item
        #         value = request.POST[key]
        #         try:
        #             variation = Variation.objects.get(product=product,
        #                                               variation_category__iexact=key,  variation_value__iexact=value)
        #             product_variation.append(variation)
        #         except Variation.DoesNotExist:
        #             pass

        # ? if the URL is something like /add_cart/?color=red&size=large, request.GET['color']
        # return HttpResponse(color, size)
        # exit()

        # ! We don't need 'cart id' anymore. Because we are using 'user id'
        # try:
        #     # ? Get the cart using the cart_id present in the session
        #     cart = Cart.objects.get(cart_id=_cart_id(request))
        # except Cart.DoesNotExist:
        #     cart = Cart.objects.create(cart_id=_cart_id(request))
        # cart.save()

        is_cart_item_exists = CartItem.objects.filter(
            product=product, user=current_user).exists()
        # ? This is return the True of False value
        # ? If we have any cart items, then we are going to go inside.
        if is_cart_item_exists:
            cart_item = CartItem.objects.filter(
                product=product, user=current_user)
            # existing_variation -> coming from the database
            # current_variations -> coming from the 'product_variation'
            # item_id -> from database

        # ? If current_variations is inside of the existing_variations, then we are going to increase of the cart item.
            ex_var_list = []
            id = []
            for item in cart_item:
                existing_variation = item.variation.all()
                ex_var_list.append(list(existing_variation))
                id.append(item.id)
        # ? it's comparing two lists. The ex_var_list contains querysets

            if product_variation in ex_var_list:
                # ? Another method : if list(product_variation) in [list(existing_variations) for existing_variations in ex_var_list]:
                # Increase the cart item quantity
                index = ex_var_list.index(product_variation)
                item_id = id[index]
                item = CartItem.objects.get(product=product, id=item_id)
                item.quantity += 1
                item.save()

            else:
                # create a new cart item.
                item = CartItem.objects.create(
                    product=product, quantity=1, user=current_user)
                if len(product_variation) > 0:
                    item.variation.clear()
                    item.variation.add(*product_variation)
            # cart_item.quantity += 1 => Because I added the quantity in cart_item(quantity=1). I don't need this one.
                    item.save()

        else:
            cart_item = CartItem.objects.create(
                product=product,
                user=current_user,
                quantity=1)
            if len(product_variation) > 0:
                cart_item.variation.clear()
                cart_item.variation.add(*product_variation)
            cart_item.save()

            return redirect('cart')

#! If the user is not authenticated,
    else:
        # ? [product_variation = []]For making a list of variations. I added after try 'product_variation.append(variation)'
        # product_variation = []

        # if request.method == 'POST':
        #     # color = request.POST['color']
        #     # size = request.POST['size']
        #     for item in request.POST:
        #         key = item
        #         value = request.POST[key]
        #         try:
        #             variation = Variation.objects.get(product=product,
        #                                               variation_category__iexact=key,  variation_value__iexact=value)
        #             product_variation.append(variation)
        #         except:
        #             pass

        # ? if the URL is something like /add_cart/?color=red&size=large, request.GET['color']
        # return HttpResponse(color, size)
        # exit()

        try:
            # ? Get the cart using the cart_id present in the session
            cart = Cart.objects.get(cart_id=_cart_id(request))
        except Cart.DoesNotExist:
            cart = Cart.objects.create(cart_id=_cart_id(request))
        cart.save()

        is_cart_item_exists = CartItem.objects.filter(
            product=product, cart=cart).exists()
        # ? This is return the True of False value
        # ? If we have any cart items, then we are going to go inside.
        if is_cart_item_exists:
            cart_item = CartItem.objects.filter(
                product=product, cart=cart)
            # existing_variation -> coming from the database
            # current_variations -> coming from the 'product_variation'
            # item_id -> from database

        # ? If current_variations is inside of the existing_variations, then we are going to increase of the cart item.
            ex_var_list = []
            id = []
            for item in cart_item:
                existing_variation = item.variation.all()
                ex_var_list.append(list(existing_variation))
                id.append(item.id)
        # ? it's comparing two lists. The ex_var_list contains querysets

            print(ex_var_list)

            if product_variation in ex_var_list:
                # ? Another method : if list(product_variation) in [list(existing_variations) for existing_variations in ex_var_list]:
                # Increase the cart item quantity
                index = ex_var_list.index(product_variation)
                item_id = id[index]
                item = CartItem.objects.get(product=product, id=item_id)
                item.quantity += 1
                item.save()

            else:
                # create a new cart item.
                item = CartItem.objects.create(
                    product=product, quantity=1, cart=cart)
                if len(product_variation) > 0:
                    item.variation.clear()
                    item.variation.add(*product_variation)
            # cart_item.quantity += 1 => Because I added the quantity in cart_item(quantity=1). I don't need this one.
                    item.save()
        else:
            cart_item = CartItem.objects.create(
                product=product,
                cart=cart,
                quantity=1)
            if len(product_variation) > 0:
                cart_item.variation.clear()
                cart_item.variation.add(*product_variation)
            cart_item.save()
    # // return HttpResponse(cart_item.quantity)
    return redirect('cart')


# ? -(minus) button in Cart. Decreasing cart items is cart.html


def remove_cart(request, product_id, cart_item_id):
    # 'cart_item_id' => path('remove_cart/<int:product_id>/<int:cart_item_id>/', views.remove_cart, name='remove_cart'),
    product = get_object_or_404(Product, id=product_id)

    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(
                product=product, user=request.user, id=cart_item_id)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_item = CartItem.objects.get(
                product=product, cart=cart, id=cart_item_id)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
    return redirect('cart')


'''
The reason for using get_object_or_404 in this context is to handle the case 
where a user tries to remove a product from the cart, 
but the specified product ID doesn't correspond to any existing product 
in the database. =>지정된 제품 ID가 데이터베이스에 존재하지 않을 때의 경우를 처리하기 위함입니다.
Using get_object_or_404 simplifies the code by handling 
the 404 error automatically and providing a clean way to handle such cases.
요약하면 '사용자 입력'을 기반으로 객체를 검색할 때 get_object_or_404를 사용하는 것이 좋은 실천 방법입니다.
이는 요청된 객체가 데이터베이스에 존재하지 않는 경우를 우아하게 처리하며 404 응답을 반환하여 
서버 오류가 발생하는 대신 더 사용자 친화적인 경험을 제공합니다.
'''

# REMOVE button


def remove_cart_item(request, product_id, cart_item_id):
    product = get_object_or_404(Product, id=product_id)
    if request.user.is_authenticated:
        cart_item = CartItem.objects.get(
            product=product, user=request.user, id=cart_item_id)
    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_item = CartItem.objects.get(
            product=product, cart=cart, id=cart_item_id)
    cart_item.delete()
    return redirect('cart')
# def remove_cart_item(request, product_id, cart_item_id):

#     product = get_object_or_404(Product, id=product_id)

#     if request.user.is_authenticated:
#         cart_item = CartItem.objects.get(
#             product=product, user=request.user, id=cart_item_id)
#     else:
#         cart = Cart.objects.get(cart_id=_cart_id(request))
#         cart_item = CartItem.objects.get(
#             product=product, cart=cart, id=cart_item_id)

#         # Print debug information
#     cart_item.delete()

# I got an error 'MultipleObjectsReturned' Because I use 'cart_item = CartItem.objects.get'
# ? To handle this situation, you should use filter() instead of get() when dealing with multiple objects.
# ? Because I'm remove multiple cart items.

    return redirect('cart')


def cart(request, total=0, quantity=0, cart_items=None):
    total = 0
    quantity = 0
    tax = 0
    grand_total = 0
    cart_items = None

    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user, is_active=True)
    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)

    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
# ? The loop is used to accumulate the total and quantity values for all items in the cart.
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (13 * total) / 100
        grand_total = total + tax
    except ObjectDoesNotExist:
        pass  # just ignore
    '''
    " for cart_item in cart_items: " 
    ==>The loop is used to accumulate the total and quantity values for all items in the cart.
    Instead of for loop, I can use the code below. 
    total = sum(cart_item.product.price * cart_item.quantity for cart_item in cart_items)
    quantity = sum(cart_item.quantity for cart_item in cart_items)
    '''
    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total,
    }

    return render(request, 'store/cart.html', context)


@login_required(login_url='login')
def checkout(request, total=0, quantity=0, cart_items=None):
    tax = 0
    grand_total = 0
    try:
        # // tax = 0
        # // grand_total = 0
        # cart = Cart.objects.get(cart_id=_cart_id(request))
        # cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(
                user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
# ? The loop is used to accumulate the total and quantity values for all items in the cart.
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (13 * total) / 100
        grand_total = total + tax
    except ObjectDoesNotExist:
        pass  # just ignore

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        # Set a default value if grand_total is not defined,
        'grand_total': grand_total,
    }
    return render(request, 'store/checkout.html', context)


'''
locals() is a Python built-in function that returns a dictionary representing the current local symbol table. It contains all the variables defined in the current scope.
'''
