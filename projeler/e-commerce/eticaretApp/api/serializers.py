from django.contrib.auth.models import User
from .models import Category,Product,ProductImage
from rest_framework import serializers

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"]
        )
        return user
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=["id","email","username"]
        
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields=[
            "id",
            "name",
            "created_at"
            ]
        
class ProductSerializer(serializers.ModelSerializer):
    user=serializers.ReadOnlyField(source="user.username")
    class Meta:
        model=Product
        fields=[
            "id",
            "user",
            "category",
            "title",
            "description",
            "price",
            "stock",
            "created_at",
            "updated_at",
            "is_active"
        ]
        read_only_fields=["id","user","created_at","updated_at"]
        
        
        
        

    
        
