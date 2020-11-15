from django.core.exceptions import ImproperlyConfigured
from django.contrib import messages
from django.db.models import Q
from django.http import Http404
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from rest_framework import filters
from rest_framework import generics
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.reverse import reverse as api_reverse
from rest_framework.views import APIView

from .models import Product, Category
from .serializers import (
		CategorySerializer, 
		ProductSerializer,
        ProductDetailSerializer
		)

class APIHomeView(APIView):
    def get(self, request, format=None):
        data = {
            'products': {
                'count': Product.objects.all().count(),
                'url': api_reverse('product-list', request=request)
            },
            'categories': {
                'count': Category.objects.all().count(),
                'url': api_reverse('categories-list', request=request)
            },
        }
        return Response(data)

class CategoryListAPIView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    # add pagination class

class ProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # more attributes to be added

class ProductRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer