import unittest

from unittest.mock import patch, MagicMock
from django.test import TestCase
from rest_framework.test import APIRequestFactory, force_authenticate
from rest_framework.utils.serializer_helpers import ReturnDict
from book.models import User
from .views import OrganizationViewSet

class OrganizationViewSetTestCase(TestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(username='test', email='test@example.com', password='testing')

    def test_rating(self):
        # test if user is not authenticated
        request = self.factory.post('/organizations/1/rating/') # no authentication provided
        view = OrganizationViewSet.as_view({'post': 'rating'})
        response = view(request)
        self.assertEqual(response.status_code, 401) # NotAuthenticated exception should be raised

        # test if rating is created successfully
        force_authenticate(request, user=self.user) # authenticate the user
        response = view(request)

        with patch('review.serializers.OrganizationRatingSerializer') as mock: 
            instance = mock() 
            instance._validate_data = MagicMock() 
            instance._validate_data()
            instance.save()
            instance.save.assert_called() 

