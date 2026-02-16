from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.utils.text import slugify
from .models import Categories, Products, CustomUser, Cart, CartItem, Order, OrderItem, Reviews, Notification

UserModel = get_user_model()


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('address',)
        read_only = ('phone_number',)


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ('receiver', 'order', 'type')
        read_only = ('sender', 'created_at')

class ProductsSerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Products
        fields = ('name', 'category', 'category_name', 'price', 'description', 'discount_price', 'special_offer', 'image', 'stock', 'is_active', 'slug')
        read_only = ('created_at', 'updated_at')


class CategoriesSerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(read_only=True)
    class Meta:
        model = Categories
        fields = ('name', 'slug')
        read_only = ('parent')



class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):

        user = UserModel.objects.create_user(
            username= validated_data['username'],
            password= validated_data['password']
        )

        return user

    class Meta:
        model = CustomUser
        fields = ('username', 'phone_number', 'password', 'address')


class UpdatePasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(required=True)
    brand_new_password = serializers.CharField(required=True, validators=[validate_password])
    confirm_password = serializers.CharField(required=True)

    def validate(self, attrs):
        if attrs['brand_new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError({'confirm_password' : " the passwords didn't match" })
        return attrs


class CartItemSerializer(serializers.ModelSerializer):
    product = serializers.SlugRelatedField(slug_field='slug', queryset=Products.objects.all(), write_only=True)
    product_details = ProductsSerializer(source='product', read_only=True)
    class Meta:
        model = CartItem
        fields = ('id', 'product_details', 'product', 'quantity')

class LoginWithCodeSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=6, required=True)

class CartSerializer(serializers.ModelSerializer):
    total_price = serializers.SerializerMethodField()
    items = CartItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = Cart
        fields = ('id','user', 'items', 'total_price')

    def get_total_price(self, obj):
        return sum(item.total_price for item in obj.cartitems.all())


class CheckoutSerializer(serializers.ModelSerializer):
    # address = serializers.CharField(max_length=150, required=True)
    cart_items = serializers.ListField(
        child=serializers.IntegerField()
    )
    
    class Meta:
        model = Order
        fields = ('address', 'cart_items')
        read_only = ('user', 'total_price', 'status', 'created_at')


class OrderSerializer(serializers.ModelSerializer):
    address = serializers.CharField(max_length = 50, required=True)
    class Meta:
        model = Order
        fields = ('address', 'total_price')
        read_only = ('created_at', 'user', 'status',)


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductsSerializer(read_only=True)
    class Meta:
        model = OrderItem
        fields = ('order', 'product', 'quantity', 'price')


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reviews
        fields = ('user', 'product', 'rating', 'comment')