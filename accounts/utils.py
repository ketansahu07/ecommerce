from django.core.mail import EmailMessage

class Util:
    @staticmethod
    def send_email(data):
        email = EmailMessage(to=[data['to']], subject=data['subject'], body=data['body'])
        email.send(fail_silently=True)
