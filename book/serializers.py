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
    activation_code = serializers.CharField(max_length=8, min_length=8, required=True)
    password = serializers.CharField(min_length=8, required=True)
    password_confirm = serializers.CharField(min_length=8, required=True)


    class Meta:
        model = User
        fields = ('activation_code', 'password', 'password_confirm')

    
    def validate_code(self, activation_code):
        if not User.objects.filter(activation_code=activation_code).exists():
            raise serializers.ValidationError('Пользователя с таким codes не найден')

        return activation_code


    def validate(self, attrs):
        pass1 = attrs.get('password')
        pass2 = attrs.pop('password_confirm')

        if pass1 != pass2:
            raise serializers.ValidationError("Password don't match")

        return attrs
    

    def save(self, **kwargs):
        data = self.validated_data
        code = data.get('code')
        password = data.get('password')

        try:
            user = User.objects.get(activation_code=code)
        
            if not user:
                raise serializers.ValidationError('Пользователь не найден')
        
        except User.DoesNotExist:
            raise serializers.ValidationError('Пользователь не найден')
        
        user.set_password(password)
        user.save()
        
        return user


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email', 'picture')

    
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['rating'] = instance.average_rating

        return rep