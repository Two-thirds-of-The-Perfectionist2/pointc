from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Organization, Product
from .serializers import OrganizationSerializer,ProductSerializer
from .permissions import IsAuthorOrReadOnly

class OrginizationViewSet(ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer

    def get_permissions(self):
        return [IsAuthorOrReadOnly()]

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    @action(['GET'], detail=False)
    def search(self, request):
        q = request.query_params.get('q')

        if q:
            queryset = queryset.filter(title__icontains=q)

        pagination = self.paginate_queryset(queryset)
        if pagination:
            serializer = self.get_serializer(pagination, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=200)
