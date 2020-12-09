import ast  # abstract syntex tree
import base64
import braintree

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse
from django.http import HttpResponseRedirect, Http404, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect 
from django.views.generic.base import View 
from django.views.generic.detail import SingleObjectMixin, DetailView 
from django.views.generic.edit import FormMixin 

from rest_framework import filters 
from rest_framework import generics 
from rest_framework import status
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.reverse import reverse as api_reverse
from rest_framework.views import APIView

from orders.forms import GuestCheckoutForm
from orders.mixins import CartOrderMixin
from orders.models import UserCheckout, Order, UserAddress
from orders.serializers import OrderSerializer, FinalizedOrderSerializer
from products.models import Variation

from .mixins import TokenMixin, CartUpdateAPIMixin, CartTokenMixin
from .models import Cart, CartItem
from .serializers import CartItemSerializer, CheckoutSerializer


class CheckoutFinalizeAPIView(TokenMixin, APIView):
    def get(self, request, format=None):
        response = {}
        order_token = request.GET.get('order_token')
        if order_token:
            checkout_id = self.parse_token(order_token).get("user_checkout_id")
            if checkout_id:
                checkout = UserCheckout.objects.get(id=checkout_id)
                client_token = checkout.get_client_token()
                response["client_token"] = client_token
                return Response(response)
        else:
            response["message"] = "This method is not allowed"
            return Response(response, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def post(self, request, format=None):
        data = request.data
        response = {}
        serializer = FinalizedOrderSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            request_data = serializer.data
            order_id = request_data.get("order_id")
            order = Order.objects.get(id=order_id)
            if not order.is_complete:   #is_complete is a method used @property in order model
                order_total = order.order_total
                nonce = request_data.get("payment_method_nonce")
                if nonce:
                    result = braintree.Transaction.sale({
                        'amount': order_total,
                        'payment_method_nonce': nonce,
                        'billing': {
                            'postal_code': f'{order.billing_address.zipcode}',
                        },
                        'options': {
                            'submit_for_settlement': True
                        }
                    })
                    success = result.is_success
                    if success:
                        # result.transiction.id to order
                        order.mark_completed(order_id=result.transaction.id)
                        order.cart.is_complete()
                        response['message'] = 'Your order has been completed.'
                        response['final_order_id'] = order.order_id
                        response['success'] = True
                    else:
                        error_message = result.message
                        response['message'] = error_message
                        response['success'] = False
            else:
                response['message'] = 'Order has already been completed.'
                response['success'] = False

        return Response(response)


class CheckoutAPIView(TokenMixin, APIView):
    def post(self, request, format=None):
        data = request.data
        serializer = CheckoutSerializer(data=data)
        order_token = None
        if serializer.is_valid():
            data = serializer.data
            user_checkout_id = data.get('user_checkout_id')
            cart_id = data.get('cart_id')
            billing_address = data.get('billing_address')
            shipping_address = data.get('shipping_address')

            user_checkout = UserCheckout.objects.get(id=user_checkout_id)
            cart_obj = Cart.objects.get(id=cart_id)
            s_a = UserAddress.objects.get(id=shipping_address)
            b_a = UserAddress.objects.get(id=billing_address)
            order, created = Order.objects.get_or_create(cart=cart_obj, user=user_checkout)
            if not order.is_complete:
                order.shipping_address = s_a
                order.billing_address = b_a
                order.save()
                order_data = {
                    'order_id': order.id,
                    'user_checkout_id': user_checkout_id
                }
                order_token = self.create_token(order_data)
        response = {
            'order_token': order_token
        }
        return Response(response)


class CartAPIView(CartTokenMixin, CartUpdateAPIMixin, APIView):
    # authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
    token_param = 'token'
    cart = None
    def get_cart(self):
        # data, cart_obj, response_status = self.get_cart_from_token()    # method in CartTokenMixin
        try:
            cart_obj = Cart.objects.get(user=self.request.user, active=True)
        except:
            cart_obj = None
        if cart_obj == None or not cart_obj.active:
            cart = Cart()
            cart.tax_percentage = 0.075     # should be changed as per the country
            if self.request.user.is_authenticated:
                cart.user = self.request.user
            cart.save()
            data = {
                'cart_id': str(cart.id)
            }
            self.create_token(data)     # method in TokenMixin and since the CartTokenMixin subclass TokenMixin, it also has this method
            cart_obj = cart

        return cart_obj

    def get(self, request, format=None):
        cart = self.get_cart()
        self.cart = cart
        self.update_cart()  # method in CartUpdateAPIMixin
        cart.save()
        # token = self.create_token(cart.id)
        items = CartItemSerializer(cart.cartitem_set.all(), many=True)
        # print(cart.items.all())
        data = {
            # 'token': self.token,          # token is needed in case when the user can buy without logging in
            'cart': cart.id,
            'total': cart.total,
            'subtotal': cart.subtotal,
            'tax_total':cart.tax_total,
            'count': cart.items.count(),
            'items': items.data
        }
        return Response(data)


if settings.DEBUG:
    braintree.Configuration.configure(braintree.Environment.Sandbox,
        merchant_id=settings.BRAINTREE_MERCHANT_ID,
        public_key=settings.BRAINTREE_PUBLIC,
        private_key=settings.BRAINTREE_PRIVATE
        )
