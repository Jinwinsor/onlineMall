from django.db import models
from django.urls import reverse
# Create your models here.


class Category(models.Model):
    category_name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    # changed from CharField => SlugField
    # Also, go to 'admin.py' add class CategoryAdmin
    description = models.CharField(max_length=250, blank=True)
    cat_image = models.ImageField(upload_to='photos/categories/', blank=True)
# For setting Images field, need to set up 'pillow': pip install pillow

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'categories'
# For changing Django_admin Category name. Categorys [Typo! looks bad]=> Categories

    def get_url(self):
        return reverse('product_by_category', args=[self.slug])
    # reverse : generate URLs for Django views.
    # store - urls.py => product_by_category

    def __str__(self):
        return self.category_name


'''
'reverse' function:
Django views. Instead of hardcoding URLs in your code, 
which can make it harder to maintain if the URL patterns change, 
you can use the reverse function to dynamically generate URLs based on 
the view's name or the URL pattern's name.

from django.urls import reverse
from django.http import HttpResponseRedirect

def my_view(request):
    # Some processing...

    # Redirect to a URL named 'another-view-name'
    url = reverse('another-view-name')
    return HttpResponseRedirect(url)

'''
