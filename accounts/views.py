from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site


from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.reverse import reverse


from rest_framework_jwt.settings import api_settings


from .serializers import RegisterSerializer
from .utils import Util


User = get_user_model()
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

class RegisterView(GenericAPIView):
    serializer_class = RegisterSerializer
    
    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        user = User.objects.get(email=user_data['email'])
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        current_site = get_current_site(request).domain
        relativelink = reverse('verify_email')
        absurl = 'http://' + current_site + relativelink + '?token=' + token
        email_body = 'Hi ' + user.username + '!\nUse the link below to verify your email\n' + absurl
        email_data = {'to': user.email,
                      'subject': 'Verify your email',
                      'body': email_body}
        
        Util.send_email(email_data)

        user_data['message'] = 'Please check you email to verify the account.'

        return Response(user_data, status=status.HTTP_201_CREATED)


class VerifyEmail(GenericAPIView):
    def get(self, request):
        pass