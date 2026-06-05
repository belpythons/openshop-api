from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    _links = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = '__all__'

    def get__links(self, obj):
        product_id = str(obj.id)
        return [
            {"rel": "self", "href": "http://localhost:8000/products", "action": "POST", "types": ["application/json"]},
            {"rel": "self", "href": f"http://localhost:8000/products/{product_id}/", "action": "GET", "types": ["application/json"]},
            {"rel": "self", "href": f"http://localhost:8000/products/{product_id}/", "action": "PUT", "types": ["application/json"]},
            {"rel": "self", "href": f"http://localhost:8000/products/{product_id}/", "action": "DELETE", "types": ["application/json"]}
        ]
