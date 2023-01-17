from rest_framework import serializers

from .models import OrganizationComment, OrganizationRating, UserRating


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrganizationComment
        exclude = ('user',)
    

    def validate(self, attrs):
        attrs = super().validate(attrs)
        request = self.context.get('request')
        attrs['user'] = request.user

        return attrs
    

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['user'] = instance.user.email

        return rep


class CustomerRatingSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserRating
        exclude = ('customer',)
    

    def validate(self, attrs):
        attrs = super().validate(attrs)
        request = self.context.get('request')
        attrs['user'] = request.user

        return attrs
    

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['user'] = instance.customer.email

        return rep


class DeliverymanRatingSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserRating
        exclude = ('deliveryman',)
    

    def validate(self, attrs):
        attrs = super().validate(attrs)
        request = self.context.get('request')
        attrs['user'] = request.user

        return attrs
    

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['user'] = instance.deliveryman.email

        return rep


class OrganizationRatingSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrganizationRating
        exclude = ('user', 'organization')
    

    def validate(self, attrs):
        attrs = super().validate(attrs)
        request = self.context.get('request')
        attrs['user'] = request.user

        return attrs
    

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['user'] = instance.user.email

        return rep
