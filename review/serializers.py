from rest_framework import serializers

from .models import OrganizationComment


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrganizationComment
        exclude = ('user_id', )
    

    def validate(self, attrs):
        attrs = super().validate(attrs)
        request = self.context.get('request')
        attrs['user'] = request.user

        return attrs
    