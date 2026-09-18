from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import RegisterSerializer,UserSerializer,CategorySerializer,ProductSerializer
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Category,Product,ProductImage


class RegisterView(APIView):
    permission_classes = [AllowAny]    
    
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {
                    "message": "User Created Success",
                    "user": serializer.data  
                },
                status=status.HTTP_201_CREATED
            )
        
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST  
        )

class LoginView(APIView):
    permission_classes=[AllowAny]
    def post(self,request):
        username=request.data.get("username")
        password=request.data.get("password")
        if not username or not password:
            return Response(
                {
                    "message":"Username or Pasword mistake request",
                    
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        user=authenticate(username=username,password=password)
        if user is None:
            return Response(
                {
                    "message": "Invalid credientials"
                },status=status.HTTP_401_UNAUTHORIZED
            )
        token=RefreshToken.for_user(user)
        loginSerializer=UserSerializer(user).data
        
        return Response(
            {
                "access_token":str(token.access_token),
                "refresh":str(token),
                "message":"Login Successfull",
                "user":loginSerializer
                
            },status=status.HTTP_200_OK
        )
class ProfileView(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        dataSerializer=UserSerializer(request.user)
        return Response(
            {
                "user":dataSerializer.data
            },status=status.HTTP_200_OK
        )

class CategoryListView(APIView):
    permission_classes=[AllowAny]
    def get(self,request):
        categories=Category.objects.all()
        dataSerializer=CategorySerializer(categories,many=True)
        return Response(
            {
                "category":dataSerializer.data
            },status=status.HTTP_200_OK           
        )

class ProductListView(APIView):
    permission_classes=[AllowAny]
    def get(self,request):
        products=Product.objects.all()
        dataSerializer=ProductSerializer(products,many=True)
        return Response(
            {
                "products":dataSerializer.data
            },status=status.HTTP_200_OK
        
        )


class ProductDetailView(APIView):
    permission_classes=[AllowAny]
    def get(self,request,id):
        try:
            product=Product.objects.get(id=id)
        except Product.DoesNotExist:
            return Response(
                {
                    "message":"Product not found"
                },status=status.HTTP_404_NOT_FOUND
            )
        dataSerializer=ProductSerializer(product)
        return Response(
            {
                "product":dataSerializer.data
            },status=status.HTTP_200_OK
        )
        
class UserProductsView(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        user=request.user
        products=Product.objects.filter(user=user)
        dataSerializer=ProductSerializer(products,many=True)
        return Response(
            {
                "products":dataSerializer.data
            },status=status.HTTP_200_OK
        )
    def post(self,request):
        user=request.user
        data=request.data.copy()
        data['user']=user.id
        serializer=ProductSerializer(data=data)
        if serializer.is_valid():
            product=serializer.save()
            return Response(
                {
                    "message":"Product created successfully",
                    "product":serializer.data
                },status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    def put(self,request,id):
        user=request.user
        try:
            product=Product.objects.get(id=id,user=user)
        except Product.DoesNotExist:
            return Response(
                {
                    "message":"Product not found"
                },status=status.HTTP_404_NOT_FOUND
            )
        data=request.data.copy()
        data['user']=user.id
        serializer=ProductSerializer(product,data=data,partial=True)
        if serializer.is_valid():
            product=serializer.save()
            return Response(
                {
                    "message":"Product updated successfully",
                    "product":serializer.data
                },status=status.HTTP_200_OK
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class UserProductsDetailView(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request,id):
        user=request.user
        try:
            product=Product.objects.get(id=id,user=user)
        except Product.DoesNotExist:
            return Response(
                {
                    "message":"Product not found"
                },status=status.HTTP_404_NOT_FOUND
            )
        dataSerializer=ProductSerializer(product)
        return Response(
            {
                "product":dataSerializer.data
            },status=status.HTTP_200_OK
        )
