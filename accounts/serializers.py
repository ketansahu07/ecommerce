from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(max_length=255, min_length=2)
    last_name = serializers.CharField(max_length=255, min_length=2)
    email = serializers.EmailField(max_length=255, min_length=4)
    password = serializers.CharField(max_length=65, min_length=8, write_only=True)
    repassword = serializers.CharField(max_length=65, min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'repassword']

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
        user.is_active = False
        user.save()
        return user