from django.core.mail import EmailMessage


from django.utils import timezone
from orders.models import UserCheckout


class Util:
    @staticmethod
    def send_email(data):
        email = EmailMessage(to=[data['to']], subject=data['subject'], body=data['body'])
        email.send(fail_silently=True)


def jwt_response_payload_handler(token, user, request, *args, **kwargs):
    
    data = {
        'token': token,
        'user_id': user.id,
        'username': user.username,
        'cart_id': 'cart id if it exists',
        'orig_iat': timezone.now(),
        # 'user_braintree_id': UserCheckout.objects.get(user=user).get_braintree_id
    }
    return data 