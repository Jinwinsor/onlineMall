from django.db import models
from store.models import Product, Variation
from accounts.models import Account

# Create your models here.


class Cart(models.Model):
    cart_id = models.CharField(max_length=250)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.cart_id


class CartItem(models.Model):
    # Explain of why I need to use 'user' in CartItem funtion. Check below.
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation = models.ManyToManyField(Variation, blank=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField(default=1)
    is_active = models.BooleanField(default=True)

    def sub_total(self):
        return self.product.price * self.quantity

    def __unicode__(self):
        return self.product


'''
The reason 'user' is in CartItem function :
n the CartItem model, the user field is a foreign key to the Account model, representing the user associated with the cart item. Including the user field in the CartItem model allows you to associate each cart item with a specific user.
If you have multiple users interacting with your website simultaneously, you'd want to ensure that each user's cart items are distinct and tied to their account. Without the user field, it would be challenging to distinguish between cart items for different users.
'''
