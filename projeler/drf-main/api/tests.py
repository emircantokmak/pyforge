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