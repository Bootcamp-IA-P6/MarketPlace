from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError

class Location(models.Model):
    city_name = models.CharField(max_length=255)
    country_name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.city_name}, {self.country_name}"


class UserProfile(models.Model):
    user = models.OneToOneField(
    User,
    on_delete=models.CASCADE,
    primary_key=True,
    related_name='profile'
)
    location = models.ForeignKey(Location, null=True, blank=True, on_delete=models.SET_NULL)
    is_premium = models.BooleanField(default=False)
    favorites = models.ManyToManyField('Product', related_name='favorited_by', blank=True)

    def __str__(self):
        return self.user.username



class Product(models.Model):
    seller = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='products_for_sale')
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField(default=1)
    image = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_sold = models.BooleanField(default=False)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Favorite(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')
        ordering = ['-created_at']


class Order(models.Model):
    buyer = models.ForeignKey(UserProfile, related_name='orders_bought', on_delete=models.CASCADE)
    seller = models.ForeignKey(UserProfile, related_name='orders_sold', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    total_price = models.DecimalField(max_digits=8, decimal_places=2)
    order_status = models.CharField(max_length=50, default='completed')
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self): 
        if self.buyer == self.seller: 
            raise ValidationError("The user cannot buy their own product") 
    def save(self, *args, **kwargs): 
        self.clean() 
        super().save(*args, **kwargs)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.get_or_create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()

class ShoppingCart(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='shopping_cart')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'product')
        ordering = ['-created_at']

