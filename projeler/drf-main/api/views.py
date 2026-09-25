from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status

from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import UserSerializer, RegisterSerializer
from .models import Category, Product, ProductImage,Favorite
from .serializers import CategorySerializer, ProductSerializer, ProductImageSerializer,FavoriteSerializer
from .filters import ProductFilter
from rest_framework.pagination import PageNumberPagination


# LOGIN / REGISTER PAGES


def login_page(request):
    return render(request, "api/login.html")


def register_page(request):
    return render(request, "api/register.html")




class LoginView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):

        # Request body boş mu?
        if not request.data:

            return Response(
                {
                    "success": False,
                    "message": "Login failed.",
                    "detail": "Request data cannot be empty.",
                    "errors": None
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = LoginSerializer(
            data=request.data
        )

        # Validation
        if not serializer.is_valid():

            return Response(
                {
                    "success": False,
                    "message": "Login failed.",
                    "detail": "Please check your email and password.",
                    "errors": serializer.errors
                },
                status=status.HTTP_401_UNAUTHORIZED
            )

        user = serializer.validated_data["user"]

        # JWT token oluştur
        try:

            refresh = RefreshToken.for_user(user)

            access_token = str(
                refresh.access_token
            )

            refresh_token = str(
                refresh
            )

        except Exception:

            return Response(
                {
                    "success": False,
                    "message": "Login failed.",
                    "detail": "Could not create authentication token.",
                    "errors": None
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        # Başarılı login
        return Response(
            {
                "success": True,
                "message": "Login successful.",
                "detail": "You have been logged in successfully.",
                "access": access_token,
                "refresh": refresh_token,
                "user": UserSerializer(user).data
            },
            status=status.HTTP_200_OK
        )
        
class RegisterView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):

        # Request body tamamen boş mu?
        if not request.data:

            return Response(
                {
                    "success": False,
                    "message": "Registration failed.",
                    "detail": "Request data cannot be empty.",
                    "errors": None
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = RegisterSerializer(
            data=request.data
        )

        # Serializer validation
        if not serializer.is_valid():

            return Response(
                {
                    "success": False,
                    "message": "Registration failed.",
                    "detail": "Please check the entered information.",
                    "errors": serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # Kullanıcı oluştur
        try:

            user = serializer.save()

        except Exception:

            return Response(
                {
                    "success": False,
                    "message": "Registration failed.",
                    "detail": "An error occurred while creating the user.",
                    "errors": None
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        # Başarılı
        return Response(
            {
                "success": True,
                "message": "User created successfully.",
                "detail": "Your account has been created.",
                "user": UserSerializer(user).data
            },
            status=status.HTTP_201_CREATED
        )

class LoginView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):

        email = request.data.get("email")
        password = request.data.get("password")

        if not email or not password:
            return Response(
                {
                    "message": "Login failed.",
                    "detail": "Email and password are required."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        email = email.strip().lower()

        user = User.objects.filter(email__iexact=email).first()

        if user is None:
            return Response(
                {
                    "message": "Login failed.",
                    "detail": "Invalid email or password."
                },
                status=status.HTTP_401_UNAUTHORIZED
            )

        user = authenticate(
            username=user.username,
            password=password
        )

        if user is None:
            return Response(
                {
                    "message": "Login failed.",
                    "detail": "Invalid email or password."
                },
                status=status.HTTP_401_UNAUTHORIZED
            )

        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "message": "Login successful.",
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "user": UserSerializer(user).data
            },
            status=status.HTTP_200_OK
        )


class ProfileView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        serializer = UserSerializer(request.user)

        return Response(serializer.data)


class CategoryListView(APIView):

    permission_classes = [AllowAny]

    def get(self, request):

        categories = Category.objects.all()

        serializer = CategorySerializer(
            categories,
            many=True
        )

        return Response(serializer.data)


class ProductListView(APIView):

    permission_classes = [AllowAny]

    def get(self, request):

        products = Product.objects.filter(
            is_active=True
        ).order_by("created_at")
        product_filter = ProductFilter(request.GET, queryset=products)

        products = product_filter.qs
        ordering = request.GET.get("ordering")
        
        allow_ordering_fields = ["price", "created_at", "-price", "-created_at", "title", "-title"]
        
        if ordering in allow_ordering_fields:
            products = products.order_by(ordering)
        paginator = PageNumberPagination()
        paginator.page_size = 10
        page=paginator.paginate_queryset(products, request)
        serializer = ProductSerializer(
            page,
            many=True
        )
        
        return paginator.get_paginated_response(serializer.data)


class ProductDetailView(APIView):

    permission_classes = [AllowAny]

    def get(self, request, product_id):

        try:
            product = Product.objects.get(
                id=product_id,
                is_active=True
            )

        except Product.DoesNotExist:

            return Response(
                {
                    "detail": "Product not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = ProductSerializer(product)

        return Response(serializer.data)


class UserProductView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        products = Product.objects.filter(
            user=request.user
        ).order_by("-created_at")

        serializer = ProductSerializer(
            products,
            many=True
        )

        return Response(serializer.data)

    def post(self, request):

        serializer = ProductSerializer(
            data=request.data
        )

        if serializer.is_valid():

            product = serializer.save(
                user=request.user
            )

            return Response(
                ProductSerializer(product).data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class UserProductDetailView(APIView):

    permission_classes = [IsAuthenticated]

    def get_product(self, product_id, user):

        try:
            return Product.objects.get(
                id=product_id,
                user=user
            )

        except Product.DoesNotExist:
            return None

    def put(self, request, product_id):

        product = self.get_product(
            product_id,
            request.user
        )

        if product is None:

            return Response(
                {
                    "detail": "Product not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = ProductSerializer(
            product,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():

            serializer.save()

            return Response(
                serializer.data
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, product_id):

        product = self.get_product(
            product_id,
            request.user
        )

        if product is None:

            return Response(
                {
                    "detail": "Product not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        product.delete()

        return Response(
            status=status.HTTP_204_NO_CONTENT
        )

class FavoriteView(APIView):

    permission_classes = [IsAuthenticated]

    # GET
    def get(self, request, favorite_id=None):

        # Get all favorites
        if favorite_id is None:

            favorites = Favorite.objects.filter(
                user=request.user
            ).select_related(
                "product",
                "product__category"
            ).prefetch_related(
                "product__images"
            )

            serializer = FavoriteSerializer(
                favorites,
                many=True
            )

            return Response(
                {
                    "success": True,
                    "message": "Favorites retrieved successfully.",
                    "count": favorites.count(),
                    "data": serializer.data
                },
                status=status.HTTP_200_OK
            )

        # Get one favorite
        try:

            favorite = Favorite.objects.select_related(
                "product",
                "product__category"
            ).prefetch_related(
                "product__images"
            ).get(
                id=favorite_id,
                user=request.user
            )

        except Favorite.DoesNotExist:

            return Response(
                {
                    "success": False,
                    "message": "Favorite not found.",
                    "data": None
                },
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = FavoriteSerializer(
            favorite
        )

        return Response(
            {
                "success": True,
                "message": "Favorite retrieved successfully.",
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )

    # POST
    def post(self, request):

        product_id = request.data.get("product")

        if product_id is None:

            return Response(
                {
                    "success": False,
                    "message": "Product ID is required.",
                    "data": None
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        try:

            product_id = int(product_id)

        except (ValueError, TypeError):

            return Response(
                {
                    "success": False,
                    "message": "Product ID must be a valid number.",
                    "data": None
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        try:

            product = Product.objects.get(
                id=product_id
            )

        except Product.DoesNotExist:

            return Response(
                {
                    "success": False,
                    "message": "Product not found.",
                    "data": None
                },
                status=status.HTTP_404_NOT_FOUND
            )

        if not product.is_active:

            return Response(
                {
                    "success": False,
                    "message": "This product is not active.",
                    "data": None
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        favorite = Favorite.objects.filter(
            user=request.user,
            product=product
        ).first()

        if favorite is not None:

            return Response(
                {
                    "success": False,
                    "message": "This product is already in your favorites.",
                    "data": FavoriteSerializer(
                        favorite
                    ).data
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = FavoriteSerializer(
            data={
                "product": product.id
            }
        )

        if serializer.is_valid():

            favorite = serializer.save(
                user=request.user
            )

            return Response(
                {
                    "success": True,
                    "message": "Product added to favorites successfully.",
                    "data": FavoriteSerializer(
                        favorite
                    ).data
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            {
                "success": False,
                "message": "Favorite could not be created.",
                "errors": serializer.errors,
                "data": None
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # PUT
    def put(self, request, favorite_id=None):

        if favorite_id is None:

            return Response(
                {
                    "success": False,
                    "message": "Favorite ID is required.",
                    "data": None
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        try:

            favorite = Favorite.objects.get(
                id=favorite_id,
                user=request.user
            )

        except Favorite.DoesNotExist:

            return Response(
                {
                    "success": False,
                    "message": "Favorite not found.",
                    "data": None
                },
                status=status.HTTP_404_NOT_FOUND
            )

        product_id = request.data.get("product")

        if product_id is None:

            return Response(
                {
                    "success": False,
                    "message": "Product ID is required.",
                    "data": None
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        try:

            product_id = int(product_id)

        except (ValueError, TypeError):

            return Response(
                {
                    "success": False,
                    "message": "Product ID must be a valid number.",
                    "data": None
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        try:

            product = Product.objects.get(
                id=product_id
            )

        except Product.DoesNotExist:

            return Response(
                {
                    "success": False,
                    "message": "Product not found.",
                    "data": None
                },
                status=status.HTTP_404_NOT_FOUND
            )

        if not product.is_active:

            return Response(
                {
                    "success": False,
                    "message": "This product is not active.",
                    "data": None
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        another_favorite = Favorite.objects.filter(
            user=request.user,
            product=product
        ).exclude(
            id=favorite.id
        ).first()

        if another_favorite is not None:

            return Response(
                {
                    "success": False,
                    "message": "This product is already in your favorites.",
                    "data": FavoriteSerializer(
                        another_favorite
                    ).data
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = FavoriteSerializer(
            favorite,
            data={
                "product": product.id
            }
        )

        if serializer.is_valid():

            favorite = serializer.save()

            return Response(
                {
                    "success": True,
                    "message": "Favorite updated successfully.",
                    "data": FavoriteSerializer(
                        favorite
                    ).data
                },
                status=status.HTTP_200_OK
            )

        return Response(
            {
                "success": False,
                "message": "Favorite could not be updated.",
                "errors": serializer.errors,
                "data": None
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # DELETE
    def delete(self, request, favorite_id=None):

        if favorite_id is None:

            return Response(
                {
                    "success": False,
                    "message": "Favorite ID is required.",
                    "data": None
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        try:

            favorite = Favorite.objects.select_related(
                "product"
            ).get(
                id=favorite_id,
                user=request.user
            )

        except Favorite.DoesNotExist:

            return Response(
                {
                    "success": False,
                    "message": "Favorite not found.",
                    "data": None
                },
                status=status.HTTP_404_NOT_FOUND
            )

        favorite_id = favorite.id
        product_id = favorite.product.id
        product_title = favorite.product.title

        favorite.delete()

        return Response(
            {
                "success": True,
                "message": "Product removed from favorites successfully.",
                "data": {
                    "favorite_id": favorite_id,
                    "product_id": product_id,
                    "product_title": product_title
                }
            },
            status=status.HTTP_200_OK
        )