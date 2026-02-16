from django.contrib import admin
from .models import CustomUser, Categories, Products, Cart, CartItem, Order, OrderItem, Reviews

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'phone_number', 'role']
    list_filter = ['phone_number', 'role']

@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    pass

@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    pass

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    pass

@admin.register(CartItem)
class CartItemRegister(admin.ModelAdmin):
    pass

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    pass

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    pass

@admin.register(Reviews)
class ReviewsAdmin(admin.ModelAdmin):
    pass