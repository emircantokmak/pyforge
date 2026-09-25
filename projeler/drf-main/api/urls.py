from django.urls import path

from .views import (
    login_page,
    register_page,
    RegisterView,
    LoginView,
    ProfileView,
    CategoryListView,
    ProductListView,
    ProductDetailView,
    UserProductView,
    UserProductDetailView,
    FavoriteView,
)


urlpatterns = [

  

    path(
        "login/",
        login_page,
        name="login-page"
    ),

    path(
        "register/",
        register_page,
        name="register-page"
    ),



    path(
        "api/login/",
        LoginView.as_view(),
        name="login-api"
    ),

    path(
        "api/register/",
        RegisterView.as_view(),
        name="register-api"
    ),


    path(
        "login/",
        login_page,
        name="login-page"
    ),

    path(
        "register/",
        register_page,
        name="register-page"
    ),

  

    path(
        "user/register/",
        RegisterView.as_view(),
        name="register"
    ),

    path(
        "user/login/",
        LoginView.as_view(),
        name="login"
    ),

    path(
        "user/profile/",
        ProfileView.as_view(),
        name="profile"
    ),


    path(
        "categories/",
        CategoryListView.as_view(),
        name="categories"
    ),

    

    path(
        "products/",
        ProductListView.as_view(),
        name="products"
    ),

    path(
        "products/<int:product_id>/",
        ProductDetailView.as_view(),
        name="product-detail"
    ),


    path(
        "user/products/",
        UserProductView.as_view(),
        name="user-products"
    ),

    path(
        "user/products/<int:product_id>/",
        UserProductDetailView.as_view(),
        name="user-product-detail"
    ),

    path(
        "favorites/",
        FavoriteView.as_view(),
        name="favorite-list"
    ),

    path(
    "favorites/<int:favorite_id>/",
    FavoriteView.as_view(),
    name="favorite-detail"
)


]
