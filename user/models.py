from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.utils.text import slugify
from decimal import Decimal



def no_less(value):
        if value < 1 :
            raise ValidationError('Value must be at least 1')




class CustomUser(AbstractUser):
    ROLE_CHOICES = (

        ('admin','Admin'),
        ('customer','Customer'),
    )
    
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='customer'
    )
    
    phone_number = models.TextField(max_length=20, unique=True)
    address =  models.TextField(max_length=100, null=True, blank=True)
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['username']


    def __str__(self):
        return str(self.phone_number)




class Categories(models.Model):
    name = models.TextField(max_length=100)
    slug = models.SlugField(unique=True, blank=True, verbose_name='Link-(slug)')
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children'
    )

    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    


class Products(models.Model):
    name = models.TextField(max_length=50)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=3)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(max_length=1500)
    discount_price = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True)
    special_offer = models.BooleanField(default=False)
    image = models.ImageField(upload_to='product_images/', null=True, blank=True)
    stock = models.BigIntegerField(default=0, validators=[no_less], help_text='must be 1 or more')
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Cart(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='carts')

    
    def __str__(self):
        return self.user.username
    

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='cartitems', on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveBigIntegerField(default=0)
    @property
    def total_price(self):
        return self.product.price * Decimal(self.quantity)
    
    def __str__(self):
        return str(self.product)
    

class Order(models.Model):

    STATUS_ORDER = (
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('delivered', 'Delivered'),
        ('canceled', 'Canceled')
    )

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=3, default=0)
    status = models.CharField(
        max_length=20,
        choices=STATUS_ORDER,
        default='pending'
    )
    address = models.CharField(max_length=150, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.status} - {self.user.username}"
    

class Notification(models.Model):
    NOTIFICATION_TYPE = (
        ('paid', 'paid'),
        ('canceled', 'Canceled')
    )

    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sent_notifications')
    receiver = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='received_notifications')
    type = models.CharField(max_length=20, choices=NOTIFICATION_TYPE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification from {self.order.status} for {self.receiver.username} "


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name='order_item')
    price = models.DecimalField(max_digits=10, decimal_places=3)
    quantity = models.BigIntegerField(default=1, validators=[no_less])

    def __str__(self):
        return f"{self.product.name} * {self.quantity}"
    

    

class Reviews(models.Model):
    order_item = models.OneToOneField(OrderItem, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField()
    comment = models.TextField(max_length=1000, null=True, blank=True)

    def __str__(self):
        return {self.rating}-{self.comment}