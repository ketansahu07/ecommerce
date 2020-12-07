from django.utils import timezone
from orders.models import UserCheckout

def jwt_response_payload_handler(token, user, request, *args, **kwargs):
    data = {
        'user_id': user.id,
        'username': user.first_name,
        'cart_id': 'send cart id here',
        'token': token,
        'orig_iat': timezone.now(),
        # 'user_braintree_id': UserCheckout.objects.get(user=user).get_braintree_id
    }
    return data 