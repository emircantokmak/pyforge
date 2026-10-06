from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status

from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import UserSerializer, RegisterSerializer
from .models import Category, Product, ProductImage,Favorite,Cart,CartItem
from .serializers import CategorySerializer, ProductSerializer,CartItemSerializer, ProductImageSerializer,FavoriteSerializer,CartSerializer
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
class FavoriteListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
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

        return Response(serializer.data)

    def post(self, request, product_id):
        try:
            product = Product.objects.get(
                id=product_id,
                is_active=True
            )
        except Product.DoesNotExist:
            return Response(
                {"detail": "Product not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        favorite, created = Favorite.objects.get_or_create(
            user=request.user,
            product=product
        )

        if not created:
            return Response(
                {"detail": "Product is already in favorites."},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = FavoriteSerializer(favorite)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )

    def delete(self, request, product_id):
        try:
            favorite = Favorite.objects.get(
                user=request.user,
                product_id=product_id
            )
        except Favorite.DoesNotExist:
            return Response(
                {"detail": "Favorite not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        favorite.delete()

        return Response(
            status=status.HTTP_204_NO_CONTENT
        )
class CartView(APIView):
    permission_classes=[IsAuthenticated]
    
    def get(self,request):
        cart,created=Cart.objects.get_or_create(user=request.user)
        serializer=CartSerializer(cart)
        return Response(
            {
                "success":True,
                "data":serializer.data
            },status=status.HTTP_200_OK
        )
    def post(self,request):
        product_id=request.data.get("product_id")
        quantity=request.data.get("quantity",1)
        if not product_id:
            return Response(
                {
                    "message":"Product Id Required"
                },status=status.HTTP_400_BAD_REQUEST
            )
        try:
            quantity=int(quantity)
        except (TypeError,ValueError):
            return Response({
                "message":"Quantity not correct."
            },status=status.HTTP_400_BAD_REQUEST
            )
        if quantity <= 0:
            return Response(
                {
                    "message":"Quantity not positive integer"
                },status=status.HTTP_400_BAD_REQUEST
            )
        try:
            product=Product.objects.get(id=product_id,
                                        is_active=True)
        except Product.DoesNotExist:
            return Response({
                "message":"Not Product Active"
            },status=status.HTTP_404_NOT_FOUND
            )
        if product.stock < quantity:
            return Response(
                {
                    "message":"There is not enough product in stock."
                },status=status.HTTP_400_BAD_REQUEST
            )
        cart,created=Cart.objects.get_or_create(user=request.user)
        cart_item,created=CartItem.objects.get_or_create(cart=cart,product=product,defaults={"quantity":quantity})
        if not created:
            new_quantity=cart_item.quantity+quantity
            if product.stock < new_quantity:
                
                return Response({
                    "message":"There is not enough product in stock."
                },status=status.HTTP_400_BAD_REQUEST
                )
            cart_item.quantity=new_quantity
            cart_item.save()
        serializer=CartItemSerializer(cart_item)
        return Response({
                "data":serializer.data,
                "message":"Cart success created."
            },status=status.HTTP_201_CREATED
        )
class CartDetailView(APIView):
    permission_classes=[IsAuthenticated]
    
    def getCardItem(self,request,item_id):
        
        try:
            return cart_item.objects.get(id=item_id,user=request.user)
        except DoesNotExits:
            return none
    def patch(self,request,item_id):
        cart_item=self.getCartItem(request,item_id)
        if cart_item is none:
            return Response({
                "message:":"Not Found Cart Item"
            },status=status.HTTP_404_NOT_FOUND
        )
        quantity=request.data.get("quantity")
        if quantity is none:
            return Response(
                {
                    "message:":"Not Found Quantity"
                },status=status.HTTP_404_NOT_FOUND
            )
        try:
            quantity=int(quantity)
        except TypeError,ValueError:
            return Response({
                "message:":"Type Error"
            },status=status.HTTP_400_BAD_REQUEST
            )
        if quantity <= 0:
            return Response({
                "message:":"quantity less than 0"
            },status=status.HTTP_400_BAD_REQUEST
            )
        if cart_item.Product.stock < quantity:
            return Response({
                "message:":"There is not enough product in stock."
            },status=status.HTTP_400_BAD_REQUEST) 
        cart_item.quantity=quantity
        cart_item.save()
        serializer=CartItemSerializer(cart_item)
        return Response({
            "data:":serializer.data,
            "message:":"Quantity success updated"
        },status=status.HTTP_200_OK)
        
    def delete(self,request,item_id):
        cart_item=self.getCartItem(request,item_id)
        if cart_item is none:
            return Response({
                "message:":"Not found cart item."
            },status=status.HTTP_404_NOT_FOUND) 
        cart_item.delete()
        return Response({
                "message:":"Cart Item success deleted."
            },status=status.HTTP_204_NO_CONTENT) 
        
class CartItemCreateView(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request):
        product_id=request.data.get("product_id")
        quantity=request.data.get("quantity",1)
        if not product_id:
            return Response({
                "message:":"Not found Product ID"
            },status=status.HTTP_400_BAD_REQUEST)
        try:
            quantity=int(quantity)
        except (ValueError,TypeError):
            return Response({
                "message:":"Quantity must be number"
                },status=status.HTTP_400_BAD_REQUEST)
        try:
            product=Product.objects.get(id=product_id,is_active=True) 
        except Product.DoesNotExits:
            return Response({
                "message:":"Product not found"
            },status=status.HTTP_404_NOT_FOUND)
        if quantity <=0 :
            return Response({
                "message:":"Quantity less than 0"
            },status=status.HTTP_400_BAD_REQUEST)
        if product.stock < quantity:
            return Response({
                "message:":"Insufficient stock"
            },status=status.HTTP_400_BAD_REQUEST)
        cart,created=Cart.objects.get_or_create(user=request.user)
        cart_item,created=CartItem.objects.get_or_create(cart=cart,product=product,defaults={"quantity":quantity})    
        if not created:
            new_quantity=CartItem.quantity+quantity
            if new_quantity > product.stock:
                return Response({
                    "message:":"Not enough stock"
                },status=status.HTTP_400_BAD_REQUEST)
            cart_item.quantity=new_quantity
            cart_item.save()
        serializer=CartItemSerializer(cart_item)
        return Response({
            "data:":serializer.data,
            "message:":"Success add product in cart"
        },status=status.HTTP_201_CREATED)
        
        
        
            
            
        
        