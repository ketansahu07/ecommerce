from django.conf import settings
from django.urls import include, path
# from django.conf.urls.static import static
from django.contrib import admin

from .views import ProductListAPIView, ProductRetrieveAPIView, CategoryListAPIView, APIHomeView

urlpatterns = [
    path('', APIHomeView.as_view(), name='home'),
    path('products/', ProductListAPIView.as_view(), name='product-list'),
    path('products/<int:pk>/', ProductRetrieveAPIView.as_view(), name='product-detail'),
    path('category/', CategoryListAPIView.as_view(), name='categories-list'),
]