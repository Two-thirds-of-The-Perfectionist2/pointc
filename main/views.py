from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import NotAcceptable
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import Organization, Product
from .serializers import OrganizationSerializer,ProductSerializer
from .filters import ProductFilter
from .permissions import IsAuthorOrReadOnly
from review.models import OrganizationRating, OrganizationLike, ProductFavorite
from review.serializers import OrganizationRatingSerializer, ProductFavoriteSerializer


User = get_user_model()


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

        
    @action(['POST'], detail=True)
    def rating(self, request, pk=None):
        user = request.user
        request.data._mutable = True
        request.data.update({'organization': get_object_or_404(Organization, id=pk)})
        ser = OrganizationRatingSerializer(data=request.data, context={'request':request})
        ser.is_valid(raise_exception=True)

        if OrganizationRating.objects.filter(user=user, organization__id=pk).exists():
            rating = OrganizationRating.objects.get(user=user, organization__id=pk)
            rating.value = request.data.get('value')
            rating.save()
        else:
            ser.save()
    
        return Response(status=201)

    
    @action(['POST'], detail=True)
    def like(self, request, pk=None):
        user_id = request.user.id
        user = get_object_or_404(User, id=user_id)
        organization = get_object_or_404(Organization, id=pk)

        if OrganizationLike.objects.filter(organization=organization, user=user).exists():
            OrganizationLike.objects.filter(organization=organization, user=user).delete()
        else:
            OrganizationLike.objects.create(organization=organization, user=user)

        return Response(status=201)


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filterset_class = ProductFilter

    
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


    @action(['PUT'], detail=True)
    def favorite(self, request, pk=None):
        user_id = request.user.id
        print(get_object_or_404(User, id=user_id))
        user = get_object_or_404(User, id=user_id)
        product = get_object_or_404(Product, id=pk)

        if ProductFavorite.objects.filter(product=product, user=user).exists():
            ProductFavorite.objects.filter(product=product, user=user).delete()
        else:
            ProductFavorite.objects.create(product=product, user=user)

        return Response(status=201)


    def get_permissions(self):        
        return [IsAuthorOrReadOnly()] 
