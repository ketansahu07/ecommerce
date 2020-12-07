from django.utils import timezone
from orders.models import UserCheckout
from carts.models import Cart

def get_cart_id(user):
    try:
        cart = Cart.objects.get(user=user, active=True)
        return cart.id
    except:
        return ''

def jwt_response_payload_handler(token, user, request, *args, **kwargs):
    cart_id = get_cart_id(user)
    data = {
        'user_id': user.id,
        'username': user.first_name,
        'cart_id': cart_id,
        'token': token,
        'orig_iat': timezone.now(),
        # 'user_braintree_id': UserCheckout.objects.get(user=user).get_braintree_id
    }
    return data 