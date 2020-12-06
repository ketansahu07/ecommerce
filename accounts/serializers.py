from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed


# from rest_framework_jwt.settings import api_settings
# from rest_framework_jwt.utils import jwt_decode_handler
# import jwt 


User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(max_length=255, min_length=2)
    last_name = serializers.CharField(max_length=255, min_length=2)
    email = serializers.EmailField(max_length=255, min_length=4)
    password = serializers.CharField(max_length=65, min_length=8, write_only=True)
    repassword = serializers.CharField(max_length=65, min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password', 'repassword']

    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs['password']
        repassword = attrs['repassword']
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({'error': 'Email is already in use'})
        elif password != repassword:
            raise serializers.ValidationError({'error': "Passwords didn't match"})
        del attrs['repassword']
        return super().validate(attrs)

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=4)
    password = serializers.CharField(max_length=65, min_length=8, write_only=True)
    token = serializers.CharField(max_length=555, min_length=8, read_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'token']
        
    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')
        user = auth.authenticate(email=email, password=password)
        if not user:
            raise AuthenticationFailed('Invalid credentials, try again!')
        if not user.is_verified:
            raise AuthenticationFailed('Account not verified')
        return super().validate(attrs)