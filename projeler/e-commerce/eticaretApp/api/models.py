from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Category(models.Model):
    name=models.CharField(max_length=100)
    slug=models.SlugField(unique=True)
    created_at=models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name="Category"
        verbose_name_plural="Categories"
        ordering=['name']
    def __str__(self):
        return self.name
class Product(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="product")
    category=models.ForeignKey(Category,on_delete=models.SET_NULL,null=True,blank=True,related_name="product")
    title=models.CharField(max_length=255)
    description=models.TextField(max_length=255)
    price=models.DecimalField(max_digits=12, decimal_places=2)
    stock=models.PositiveIntegerField(default=0)    
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    is_active=models.BooleanField(default=True)
    
    def __str__(self):
        return self.title
class ProductImage(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name="images")
    img=models.ImageField(upload_to="products/")
    is_main=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.product.title} - image"
    


    
    
