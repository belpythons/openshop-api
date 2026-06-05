import uuid
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Product

class ProductAPITests(APITestCase):
    def setUp(self):
        self.p1 = Product.objects.create(
            name="Laptop ASUS ROG",
            sku="SKU-ROG-01",
            shop="ASUS Official",
            location="Jakarta",
            price=15000000,
            category="Electronics",
            stock=10,
            description="Gaming Laptop",
            is_delete=False
        )
        self.p2 = Product.objects.create(
            name="iPhone 14 Pro",
            sku="SKU-IPHONE-02",
            shop="Apple Store",
            location="Bandung",
            price=20000000,
            category="Electronics",
            stock=5,
            description="Smartphone",
            is_delete=False
        )
        self.p3 = Product.objects.create(
            name="Keyboard Mechanical",
            sku="SKU-KEY-03",
            shop="Keychron Store",
            location="Jakarta",
            price=800000,
            category="Electronics",
            stock=2,
            description="Mechanical Keyboard",
            is_delete=True  # Soft-deleted
        )

    def test_list_products_excludes_soft_deleted(self):
        url = reverse('product-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("products", response.data)
        products = response.data["products"]
        self.assertEqual(len(products), 2)
        
        # Verify both self links and fields are present
        names = [p["name"] for p in products]
        self.assertIn("Laptop ASUS ROG", names)
        self.assertIn("iPhone 14 Pro", names)
        self.assertNotIn("Keyboard Mechanical", names)
        
        # Check HATEOAS links format
        links = products[0]["_links"]
        p1_id = str(self.p1.id)
        expected_links = [
            {"rel": "self", "href": "http://localhost:8000/products", "action": "POST", "types": ["application/json"]},
            {"rel": "self", "href": f"http://localhost:8000/products/{p1_id}/", "action": "GET", "types": ["application/json"]},
            {"rel": "self", "href": f"http://localhost:8000/products/{p1_id}/", "action": "PUT", "types": ["application/json"]},
            {"rel": "self", "href": f"http://localhost:8000/products/{p1_id}/", "action": "DELETE", "types": ["application/json"]}
        ]
        self.assertEqual(links, expected_links)

    def test_create_product(self):
        url = reverse('product-list')
        data = {
            "name": "Mouse Wireless Logi",
            "sku": "SKU-MOUSE-04",
            "shop": "Logitech Official",
            "location": "Surabaya",
            "price": 300000,
            "description": "Wireless Mouse",
            "category": "Electronics",
            "stock": 15
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], "Mouse Wireless Logi")
        self.assertIn("_links", response.data)
        new_id = response.data["id"]
        
        # Check that link contains new id
        links = response.data["_links"]
        self.assertEqual(links[1]["href"], f"http://localhost:8000/products/{new_id}/")

    def test_create_product_invalid_data(self):
        url = reverse('product-list')
        data = {
            "price": "not-a-number"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_detail_active_product(self):
        url = reverse('product-detail', kwargs={'pk': self.p1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Laptop ASUS ROG")

    def test_get_detail_soft_deleted_product(self):
        # Sesuai aturan, produk yang sudah di-soft delete (is_delete=True) HARUS TETAP BISA DIAKSES via endpoint detail ini.
        url = reverse('product-detail', kwargs={'pk': self.p3.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Keyboard Mechanical")
        self.assertTrue(response.data["is_delete"])

    def test_get_detail_not_found(self):
        random_uuid = uuid.uuid4()
        url = reverse('product-detail', kwargs={'pk': random_uuid})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, {"detail": "Not found."})

    def test_get_detail_invalid_uuid(self):
        url = reverse('product-detail', kwargs={'pk': "not-a-valid-uuid"})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, {"detail": "Not found."})

    def test_update_product(self):
        url = reverse('product-detail', kwargs={'pk': self.p1.id})
        data = {
            "name": "Laptop ASUS ROG Zephyrus",
            "sku": "SKU-ROG-01-NEW",
            "shop": "ASUS Official Store",
            "location": "Jakarta",
            "price": 18000000,
            "description": "High-end Gaming Laptop",
            "category": "Electronics",
            "stock": 8
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Laptop ASUS ROG Zephyrus")
        
        # Verify database update
        self.p1.refresh_from_db()
        self.assertEqual(self.p1.name, "Laptop ASUS ROG Zephyrus")

    def test_update_product_invalid_data(self):
        url = reverse('product-detail', kwargs={'pk': self.p1.id})
        data = {
            "name": "",
            "price": "invalid"
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_soft_delete_product(self):
        url = reverse('product-detail', kwargs={'pk': self.p1.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Verify soft deleted in database (is_delete=True) and not permanently deleted
        self.p1.refresh_from_db()
        self.assertTrue(self.p1.is_delete)

    def test_soft_delete_not_found(self):
        random_uuid = uuid.uuid4()
        url = reverse('product-detail', kwargs={'pk': random_uuid})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_search_filter_name(self):
        url = f"{reverse('product-list')}?name=asus"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        products = response.data["products"]
        self.assertEqual(len(products), 1)
        self.assertEqual(products[0]["name"], "Laptop ASUS ROG")

    def test_search_filter_location(self):
        url = f"{reverse('product-list')}?location=bandung"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        products = response.data["products"]
        self.assertEqual(len(products), 1)
        self.assertEqual(products[0]["name"], "iPhone 14 Pro")

    def test_search_filter_name_excludes_soft_deleted(self):
        # Keyboard Mechanical is in Jakarta, is_delete=True.
        # Searching Jakarta should return p1 but NOT p3.
        url = f"{reverse('product-list')}?location=jakarta"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        products = response.data["products"]
        self.assertEqual(len(products), 1)
        self.assertEqual(products[0]["name"], "Laptop ASUS ROG")

