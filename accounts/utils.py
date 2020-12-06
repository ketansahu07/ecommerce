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
        'user': user.first_name,
        'user_id': user.id,
        'cart_id': 'cart id if it exists',
        'token': token,
        'orig_iat': timezone.now(),
        # 'user_braintree_id': UserCheckout.objects.get(user=user).get_braintree_id
    }
    return data 