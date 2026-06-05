from django.core.management.base import BaseCommand
from products.models import Product

class Command(BaseCommand):
    help = 'Seed database with initial product data'

    def handle(self, *args, **kwargs):
        self.stdout.write("Deleting existing products...")
        Product.objects.all().delete()

        products_data = [
            {
                "name": "Kelas Belajar Python",
                "sku": "DCD01",
                "description": "Kelas pemrograman Python tingkat dasar hingga mahir di Dicoding.",
                "shop": "Dicoding",
                "location": "Bandung",
                "price": 1500000,
                "discount": 10,
                "category": "E-Learning",
                "stock": 999,
                "is_available": True,
                "picture": "https://example.com/images/python-class.png",
                "is_delete": False
            },
            {
                "name": "Laptop ASUS ROG Zephyrus",
                "sku": "ASUS-ROG-ZEP-01",
                "description": "Gaming laptop tipis dengan performa ekstrem.",
                "shop": "ASUS Store",
                "location": "Jakarta",
                "price": 28999000,
                "discount": 5,
                "category": "Electronics",
                "stock": 15,
                "is_available": True,
                "picture": "https://example.com/images/rog-zephyrus.png",
                "is_delete": False
            },
            {
                "name": "iPhone 14 Pro Max 256GB",
                "sku": "APL-IPH14PM-256",
                "description": "Apple iPhone 14 Pro Max kapasitas 256GB warna Deep Purple.",
                "shop": "Apple Store",
                "location": "Jakarta",
                "price": 21999000,
                "discount": 0,
                "category": "Electronics",
                "stock": 8,
                "is_available": True,
                "picture": "https://example.com/images/iphone14pm.png",
                "is_delete": False
            },
            {
                "name": "Keyboard Mechanical Keychron K2",
                "sku": "KCR-K2-RGB",
                "description": "Mechanical keyboard Keychron K2 layout 75% dengan switch RGB Gateron.",
                "shop": "Keychron Indonesia",
                "location": "Surabaya",
                "price": 1450000,
                "discount": 12,
                "category": "Accessories",
                "stock": 0,
                "is_available": False,
                "picture": "https://example.com/images/keychron-k2.png",
                "is_delete": False
            },
            {
                "name": "Buku Panduan Algoritma & Struktur Data",
                "sku": "BK-ASD-02",
                "description": "Buku referensi lengkap algoritma dan struktur data dalam Python.",
                "shop": "Gramedia",
                "location": "Yogyakarta",
                "price": 120000,
                "discount": 0,
                "category": "Books",
                "stock": 50,
                "is_available": True,
                "picture": "https://example.com/images/book-asd.png",
                "is_delete": True  # Soft-deleted
            }
        ]

        self.stdout.write("Seeding products...")
        created_count = 0
        for item in products_data:
            Product.objects.create(**item)
            created_count += 1

        self.stdout.write(self.style.SUCCESS(f"Successfully seeded {created_count} products."))
