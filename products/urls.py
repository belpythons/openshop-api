from django.urls import re_path
from .views import ProductList, ProductDetail

urlpatterns = [
    re_path(r'^products/?$', ProductList.as_view(), name='product-list'),
    re_path(r'^products/(?P<pk>[^/]+)/?$', ProductDetail.as_view(), name='product-detail'),
]
