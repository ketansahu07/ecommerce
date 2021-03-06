from django.core.exceptions import ImproperlyConfigured
from django.contrib import messages
from django.db.models import Q
from django.http import Http404
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.reverse import reverse as api_reverse
from rest_framework.views import APIView

from .filters import ProductFilter
from .models import Product, Category
from .serializers import (
		CategorySerializer, 
		ProductSerializer,
        ProductDetailSerializer,
        ProductDetailUpdateSerializer
		)

class APIHomeView(APIView):
    def get(self, request, format=None):
        data = {
            'auth': {
                'register': api_reverse('registration', request=request),
                # 'login': api_reverse('user_login', request=request),
                'login': api_reverse('auth_login', request=request),
                'verify-token': api_reverse('verify_token', request=request),
                'refresh-token': api_reverse('refresh_token', request=request),
                'logout': api_reverse('auth_logout', request=request),
                'user_checkout': api_reverse('user_checkout', request=request),
            },
            'products': {
                'count': Product.objects.all().count(),
                'url': api_reverse('product_list', request=request)
            },
            'categories': {
                'count': Category.objects.all().count(),
                'url': api_reverse('categories_list', request=request)
            },
            'orders': {
                'url': api_reverse('orders', request=request),
            },
            'address': {
                'url': api_reverse('user_address_list', request=request),
                'create': api_reverse('user_address_create', request=request),
            },
            'checkout': {
                'cart': api_reverse('cart', request=request),
                'checkout': api_reverse('checkout', request=request),
                'finalize': api_reverse('checkout_finalize', request=request),
            },
        }
        return Response(data)

class CategoryListAPIView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    # add pagination class

class CategoryRetrieveAPIView(generics.RetrieveAPIView):
    #authentication_classes = [SessionAuthentication]
	#permission_classes = [IsAuthenticated]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class ProductListAPIView(generics.ListAPIView):
    #permission_classes = [IsAuthenticated]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter,
                       filters.OrderingFilter,
                       DjangoFilterBackend,
                       ]
    search_fields = ['title', 'description']
    ordering_fields = ['title', 'id']
    filter_class = ProductFilter

class ProductRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer