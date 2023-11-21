from django.shortcuts import render, get_object_or_404
from .models import Product
from category.models import Category
from carts.views import _cart_id
from carts.models import CartItem
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
'''
In Django, Q is a class that is part of the django.db.models module and is used to build complex queries with OR conditions. It allows you to construct queries with multiple conditions, including OR conditions, and is particularly useful when you need to create more complex queries than those easily expressed using the regular query syntax.
'''


def store(request, category_slug=None):
    categories = None
    products = None
    if category_slug != None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(
            category=categories, is_available=True)
        paginator = Paginator(products, 6)  # 6 products per page
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()
    else:
        products = Product.objects.all().filter(
            is_available=True).order_by('id')  # 8 products
        paginator = Paginator(products, 6)  # 6 products per page
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()

    context = {
        'products': paged_products,
        'product_count': product_count,
    }
    return render(request, 'store/store.html', context)


def product_detail(request, category_slug, product_slug):
    try:
        single_product = Product.objects.get(
            category__slug=category_slug, slug=product_slug)
        in_cart = CartItem.objects.filter(
            cart__cart_id=_cart_id(request), product=single_product).exists()
        # return HttpResponse(in_cart)
        # exit() ==> It the item is in the cart, it shows 'True' or not, it 'False'
    except Exception as e:
        raise e
# category__slug : The double underscore notation is a common feature in Django's ORM (Object-Relational Mapping) to navigate and filter based on relationships between models.
# category__slug is used to filter Product objects based on the slug field of the related Category model.
    context = {
        'single_product': single_product,
        'in_cart': in_cart,
    }
    return render(request, 'store/product_detail.html', context)


def search(request):
    # <input type="text" class="form-control" style="width:60%;" placeholder="Search" name="keyword">
    if 'keyword' in request.GET:
        keyword = request.GET.get('keyword')
        if keyword:  # if keyword has something.
            products = Product.objects.order_by(
                '-created_at').filter(Q(product_name__icontains=keyword) | Q(description__icontains=keyword))
            product_count = products.count()
    context = {
        'products': products,
        'product_count': product_count,
    }

    return render(request, 'store/store.html', context)
