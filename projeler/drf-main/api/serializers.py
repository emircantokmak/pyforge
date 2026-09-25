from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Category, Product, ProductImage,Favorite


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["id", "username", "email"]

class LoginSerializer(serializers.Serializer):

    email = serializers.EmailField()

    password = serializers.CharField(
        write_only=True
    )

    def validate(self, data):

        email = data.get("email")
        password = data.get("password")

        if not email:
            raise serializers.ValidationError(
                {
                    "email": "Email is required."
                }
            )

        if not password:
            raise serializers.ValidationError(
                {
                    "password": "Password is required."
                }
            )

        email = email.strip().lower()

        user = User.objects.filter(
            email__iexact=email
        ).first()

        if user is None:

            raise serializers.ValidationError(
                {
                    "detail": "Invalid email or password."
                }
            )

        authenticated_user = authenticate(
            username=user.username,
            password=password
        )

        if authenticated_user is None:

            raise serializers.ValidationError(
                {
                    "detail": "Invalid email or password."
                }
            )

        if not authenticated_user.is_active:

            raise serializers.ValidationError(
                {
                    "detail": "This account is inactive."
                }
            )

        data["user"] = authenticated_user

        return data
    
class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        write_only=True,
        min_length=6
    )

    email = serializers.EmailField()

    class Meta:
        model = User

        fields = [
            "username",
            "email",
            "password"
        ]

    def validate_username(self, value):

        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "Username cannot be empty."
            )

        if len(value) < 3:
            raise serializers.ValidationError(
                "Username must be at least 3 characters."
            )

        if User.objects.filter(
            username__iexact=value
        ).exists():

            raise serializers.ValidationError(
                "This username is already registered."
            )

        return value

    def validate_email(self, value):

        value = value.strip().lower()

        if not value:
            raise serializers.ValidationError(
                "Email cannot be empty."
            )

        if User.objects.filter(
            email__iexact=value
        ).exists():

            raise serializers.ValidationError(
                "This email address is already registered."
            )

        return value

    def validate_password(self, value):

        if not value:
            raise serializers.ValidationError(
                "Password cannot be empty."
            )

        if len(value) < 6:
            raise serializers.ValidationError(
                "Password must be at least 6 characters."
            )

        return value

    def create(self, validated_data):

        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"]
        )

        return user
# PRODUCT

class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            "slug",
            "created_at"
        ]


# IMAGE

class ProductImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductImage
        fields = [
            "id",
            "image",
            "is_main",
            "created_at"
        ]
        read_only_fields = ["id", "created_at"]

    def create(self, validated_data):
        product = self.context["product"]

        if validated_data.get("is_main", False):
            ProductImage.objects.filter(product=product).update(is_main=False)

        return ProductImage.objects.create(product=product, **validated_data)

    def update(self, instance, validated_data):
        product = instance.product

        if validated_data.get("is_main", False):
            ProductImage.objects.filter(product=product).exclude(id=instance.id).update(is_main=False)

        return super().update(instance, validated_data)


class ProductSerializer(serializers.ModelSerializer):

    user = serializers.ReadOnlyField(source="user.username")
    images = ProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "user",
            "category",
            "title",
            "description",
            "price",
            "stock",
            "created_at",
            "updated_at",
            "is_active",
            "images"
        ]

        read_only_fields = [
            "id",
            "user",
            "images",
            "created_at",
            "updated_at",
        ]



# FAVORITE

class FavoriteSerializer(serializers.ModelSerializer):

    user = serializers.ReadOnlyField(
        source="user.username"
    )

    product_detail = ProductSerializer(
        source="product",
        read_only=True
    )

    class Meta:
        model = Favorite

        fields = [
            "id",
            "user",
            "product",
            "product_detail",
            "created_at"
        ]

        read_only_fields = [
            "id",
            "user",
            "product_detail",
            "created_at"
        ]

    def validate_product(self, value):

        if not value.is_active:
            raise serializers.ValidationError(
                "This product is not active."
            )

        return value