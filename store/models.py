from django.db import models
from category.models import Category
from django.urls import reverse

# Create your models here.


class Product(models.Model):
    product_name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(max_length=500, blank=True)
    price = models.IntegerField()
    images = models.ImageField(upload_to='photos/products')
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def get_url(self):
        return reverse('product_detail', args=[self.category.slug, self.slug])
    # [self.category.slug] : Category folder => models.py => slug
    # [self.slug] : class Product - slug
    # Why args is having two things? Because, the url. It passes category slug and product slug.
    # path('<slug:category_slug>/<slug:product_slug>/', views.product_detail, name='product_detail'),

    def __str__(self):
        return self.product_name
