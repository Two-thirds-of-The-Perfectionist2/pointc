from rest_framework.viewsets import ModelViewSet

from .models import Organization, Product
from .serializers import OrganizationSerializer,ProductSerializer

class OrginizationViewSet(ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
