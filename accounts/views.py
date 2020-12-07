from django.shortcuts import render
from django.contrib.auth import get_user_model, login
from django.contrib.sites.shortcuts import get_current_site


from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.reverse import reverse


from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.utils import jwt_decode_handler
from rest_framework_jwt.serializers import (JSONWebTokenSerializer, 
                                            VerifyJSONWebTokenSerializer)
from rest_framework_jwt.views import ObtainJSONWebToken


import jwt 


from .serializers import RegisterSerializer, LoginSerializer
from .utils import Util


User = get_user_model()


class RegisterAPIView(GenericAPIView):
    serializer_class = RegisterSerializer
    
    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        user = User.objects.get(email=user_data['email'])
        token = user.token()
        current_site = get_current_site(request).domain
        relativelink = reverse('verify_email')
        absurl = 'http://' + current_site + relativelink + '?token=' + token
        email_body = 'Hello ' + user.first_name + '!\nUse the link below to verify your email\n' + absurl
        email_data = {'to': user.email,
                      'subject': 'Verify your email',
                      'body': email_body}
        
        Util.send_email(email_data)

        user_data['message'] = 'Please check you email to verify the account.'

        return Response(user_data, status=status.HTTP_201_CREATED)


class VerifyEmailAPIView(GenericAPIView):
    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt_decode_handler(token)
            user = User.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()
            return Response({'message': 'Successfully activated!'}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError:
            return Response({'error': 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)


# THIS IS OF NO USE AS OF NOW SINCE WE ARE USING JWT OBTAIN TOKEN URL

# class LoginAPIView(GenericAPIView):
    ## serializer_class = LoginSerializer
    # serializer_class = JSONWebTokenSerializer
    # def post(self, request):
        # response = ObtainJSONWebToken.as_view()(request=request._request).data
        ## data = request.data
        ## serializer = self.serializer_class(data=data)
        ## serializer.is_valid(raise_exception=True)
        ## user = User.objects.get(email=data['email'])
        ## token = user.token()
        ## validated_data = VerifyJSONWebTokenSerializer().validate({'token': token})
        ## response = jwt_response_payload_handler(token, user, request)       # custom function in utils.py
        # return Response(response, status=status.HTTP_200_OK)