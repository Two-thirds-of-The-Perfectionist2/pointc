from rest_framework.viewsets import ModelViewSet

from .models import OrganizationCard, Products
from .serializers import OrganizationCardSerializer,ProductsSerializer

class OrginizationCardViewSet(ModelViewSet):
    queryset = OrganizationCard.objects.all()
    serializer_class = OrganizationCardSerializer


class ProductsViewSet(ModelViewSet):
    queryset = Products.objects.all()
    serializer_class = ProductsSerializer
