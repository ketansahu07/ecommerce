"""ecommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token

from carts.views import (CartAPIView,
                         CheckoutAPIView,
                         CheckoutFinalizeAPIView,
                         )

from orders.views import (UserAddressCreateAPIView,
                          UserAddressListAPIView,
                          UserCheckoutAPI,
                          OrderListAPIView,
                          OrderRetrieveAPIView,
                          )

from products.views import (APIHomeView,
                            CategoryListAPIView,
                            CategoryRetrieveAPIView,
                            ProductListAPIView,
                            ProductRetrieveAPIView,
                            )

from accounts.views import (RegisterView,
                            VerifyEmail,
                            )

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/',APIHomeView.as_view(), name='home'),
    # path('api/accounts/', include('rest_registration.api.urls')),
    path('api/auth/register/', RegisterView.as_view(), name='registration'),
    path('api/auth/verify-email/', VerifyEmail.as_view(), name='verify_email'),
    path('api/auth/token/', obtain_jwt_token, name='auth_login'),
    path('api/auth/token/refresh/', refresh_jwt_token, name='refresh_token'),
    path('api/categories/', CategoryListAPIView.as_view(), name='categories_list'),
    path('api/categories/<int:pk>/', CategoryRetrieveAPIView.as_view(), name='category_detail'),
    path('api/products/', ProductListAPIView.as_view(), name='product_list'),
    path('api/products/<int:pk>/', ProductRetrieveAPIView.as_view(), name='product_detail'),
    path('api/orders/', OrderListAPIView.as_view(), name='orders'),
    path('api/orders/<int:pk>/', OrderRetrieveAPIView.as_view(), name='order_detail'),
    path('api/user/address/', UserAddressListAPIView.as_view(), name='user_address_list'),
    path('api/user/address/create/', UserAddressCreateAPIView.as_view(), name='user_address_create'),
    path('api/user/checkout/', UserCheckoutAPI.as_view(), name='user_checkout'),
    path('api/cart/', CartAPIView.as_view(), name='cart'),
    path('api/checkout/', CheckoutAPIView.as_view(), name='checkout'),
    path('api/checkout/finalize/', CheckoutFinalizeAPIView.as_view(), name='checkout_finalize'),
]


if settings.DEBUG:
	urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)