from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import Organization, Product
from .serializers import OrganizationSerializer,ProductSerializer
from .filters import ProductFilter
from .permissions import IsAuthorOrReadOnly
from django.db.models import Q

class OrginizationViewSet(ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer

    def get_permissions(self):
        return [IsAuthorOrReadOnly()]

    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('q', openapi.IN_QUERY, type=openapi.TYPE_STRING)
    ])
    @action(['GET'], detail=False)
    def search(self, request):
        # /product/search/?q=hello
        # query_params = {'q':'hello'}
        q = request.query_params.get('q')
        # queryset = Product.objects.all()
        queryset = self.get_queryset()
        if q:
            # queryset = queryset.filter(title__icontains=q) # title ilike '%hello%'
            queryset = queryset.filter(Q(title__icontains=q) | Q(tag__icontains=q))
            # title ilike '%hello%' or description ilike '%hello%'
        # serializer = ProductSerializer(queryset, many=True)
        pagination = self.paginate_queryset(queryset)
        if pagination:
            serializer = self.get_serializer(pagination, many=True)
            return self.get_paginated_response(serializer.data)
            
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=200)


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filterset_class = ProductFilter

    def get_permissions(self):
        
        return [IsAuthorOrReadOnly()] 
    
    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('q', openapi.IN_QUERY, type=openapi.TYPE_STRING)
    ])
    @action(['GET'], detail=False)
    def search(self, request):
        # /product/search/?q=hello
        # query_params = {'q':'hello'}
        q = request.query_params.get('q')
        # queryset = Product.objects.all()
        queryset = self.get_queryset()
        if q:
            # queryset = queryset.filter(title__icontains=q) # title ilike '%hello%'
            queryset = queryset.filter(Q(title__icontains=q) | Q(description__icontains=q))
            # title ilike '%hello%' or description ilike '%hello%'
        # serializer = ProductSerializer(queryset, many=True)
        pagination = self.paginate_queryset(queryset)
        if pagination:
            serializer = self.get_serializer(pagination, many=True)
            return self.get_paginated_response(serializer.data)
            
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=200)