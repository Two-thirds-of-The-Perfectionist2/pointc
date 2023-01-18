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


class UserRatingSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserRating
        exclude = ('customer',)
    

    def validate(self, attrs):
        attrs = super().validate(attrs)
        request = self.context.get('request')
        attrs['customer'] = request.user

        return attrs
    

class OrganizationRatingSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrganizationRating
        exclude = ('user', 'organization')
    

    def validate(self, attrs):
        attrs = super().validate(attrs)
        request = self.context.get('request')
        attrs['user'] = request.user
        attrs['organization'] = request.data.get('organization')

        return attrs
    