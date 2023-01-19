from django.shortcuts import get_object_or_404
from rest_framework import serializers

from .models import User


class RegisterUserSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(min_length=8, required=True)


    class Meta:
        model = User
        fields = ('email', 'password', 'password_confirm')
    

    def validate(self, attrs):
        pass1 = attrs.get('password')
        pass2 = attrs.pop('password_confirm')

        if pass1 != pass2:
            raise serializers.ValidationError('Password do not match')
        
        return attrs
    

    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError('User with email already exists')
        
        return email
    

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class NewPasswordSerializer(serializers.Serializer):
    password_confirm = serializers.CharField(min_length=8, required=True)


    class Meta:
        model = User
        fields = ('activation_code', 'password', 'password_confirm')


    def validate(self, attrs):
        attrs =  super().validate(attrs)
        request = self.context.get('request')
        user = get_object_or_404(User, activation_code=request.data.get('activation_code'))

        pass1 = request.data.get('password')
        pass2 = attrs.pop('password_confirm')

        if pass1 != pass2:
            raise serializers.ValidationError("Password don't match")

        user.activation_code = None
        user.is_active = True
        user.set_password(pass1)
        user.save()

        return attrs


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email', 'picture')

    
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['rating'] = instance.average_rating

        return rep