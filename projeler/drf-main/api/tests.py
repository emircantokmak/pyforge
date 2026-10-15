from django.test import TestCase
from rest_framework.test import APIClient,APITestCase
from .models import Product
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status

# Create your tests here.

class ProductListAPITest(APITestCase):
    def setUp(self):
        self.client = APIClient()

        self.user = User.objects.create_user(
            username="testuser",
            password="TestPassword123"
        )

        self.product = Product.objects.create(
            user=self.user,
            title="Test Telefonu",
            description="Test açıklaması",
            price="15000.00",
            stock=10,
            is_active=True
        )

    def test_product_list_returns_200(self):
        response = self.client.get("/api/products/")

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_product_list_contains_created_product(self):
        response = self.client.get("/api/products/")

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        products = response.data["results"]

        product_titles = [
            product["title"] for product in products
        ]

        self.assertIn("Test Telefonu", product_titles)
    
    def test_product_list_excludes_inactive_products(self):
        Product.objects.create(
            user=self.user,
            title="Inactive Product",
            description="This is an inactive product",
            price="20000.00",
            stock=5,
            is_active=False
        )
        
        response = self.client.get("/api/products/")
        
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        products_titles=[product["title"] for product in response.data["results"]]
        self.assertNotIn("Inactive Product",products_titles)
        
class ProductAutherizationTest(APITestCase):
    def setUp(self):
        self.client = APIClient()

        def test_unauthanticated_user_cannot_create_product(self):
            response=self.client.post("/api/user/products/",{
                "title":"Unauthorized Product",
                "description":"This product should not be created",
                "price":"10000.00",
                "stock":5,
                "is_active":True
            },format="json")
            self.assertEqual(response.status_code, 
                            status.HTTP_401_UNAUTHORIZED)
            
        def test_authenticated_user_can_other_delete_product(self):
            user=User.objects.create_user(
                username="testuser2",
                password="TestPassword123"
            )
            
            user2=User.objects.create_user(
                username="testuser3",
                password="TestPassword123"
            )
            self.client.force_authenticate(user=user2)
            product=Product.objects.create(
                user=user,
                title="Product to Delete",
                description="This product will be deleted",
                price="12000.00",
                stock=3,
                is_active=True
            )
                        
            response=self.client.delete(f"/api/user/products/{product.id}/")
            self.assertIn(
                response.status_code,
                [status.HTTP_403_FORBIDDEN, status.HTTP_404_NOT_FOUND]
            )
            self.assertTrue(Product.objects.filter(id=product.id).exists())
            
        def test_authenticated_user_can_delete_own_product(self):
            user=User.objects.create_user(
                username="testuser4",
                password="TestPassword123"
            )
            product=Product.objects.create(
                user=user,
                title="Product to Delete",
                description="This product will be deleted",
                price="12000.00",
                stock=3,
                is_active=True
            )
            
            self.client.force_authenticate(user=user)
            
            
            response=self.client.delete(f"/api/user/products/{product.id}/")
            self.assertEqual(response.status_code,status.HTTP_204_NO_CONTENT)
            self.assertFalse(Product.objects.filter(id=product.id).exists())
            
            
class JWTAuthenticationAPITest(APITestCase):
    def setUp(self):
        self.client=APIClient()
        self.user=User.objects.create_user(
            username="jwtuser",
            password="JWTPassword123",
            email="jwtuser@example.com"
        )
    def test_login_returns_refresh_and_access_tokens(self):
        response=self.client.post("/api/user/login/",{
            "username":"jwtuser",
            "password":"JWTPassword123",
            "email":"jwtuser@example.com"
        },format="json")
        self.assertEqual(response.status_code,
                        status.HTTP_200_OK)
        self.assertIn("access",response.data)
        self.assertIn("refresh",response.data)
        self.assertIn("user",response.data)
        
    def test_access_token_allows_authenticated_requests(self):
        response=self.client.post("/api/user/login/",{
            "username":"jwtuser",
            "password":"JWTPassword123",
            "email":"jwtuser@example.com"
        },format="json")
        access_token=response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
        profile_response=self.client.get("/api/user/profile/")
        self.assertEqual(profile_response.status_code,
                        status.HTTP_200_OK)
        self.assertEqual(profile_response.data["username"],"jwtuser")
        
    def test_login_rejects_incorrect_password(self):
        response=self.client.post("/api/user/login/",{
            "username":"jwtuser",
            "password":"WrongPassword",
            "email":"jwtuser@example.com"
        },format="json")
        self.assertEqual(response.status_code,
                        status.HTTP_401_UNAUTHORIZED)
        self.assertNotIn("access", response.data)
        self.assertNotIn("refresh", response.data)

        