from django.urls import path
from .views import RegisterView,LoginView,ProfileView,CategoryListView,ProductListView,ProductDetailView,UserProductsView,UserProductsDetailView
urlpatterns = [
    path('user/register',RegisterView.as_view(),name="register"),
    path('user/login',LoginView.as_view(),name="login"),
    path('user/profile',ProfileView.as_view(),name="profile"),
    path('category',CategoryListView.as_view(),name="category_list"),
    path('products',ProductListView.as_view(),name="product_list"),
    path('products/<int:id>',ProductDetailView.as_view(),name="product_detail"),
    path('user/products',UserProductsView.as_view(),name="user_products"),
    path('user/products/<int:id>', UserProductsDetailView.as_view(), name="user_product_detail"),
    
]
