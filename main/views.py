from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.http.request import QueryDict
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.exceptions import NotAcceptable, NotFound
from rest_framework.pagination import PageNumberPagination
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import Organization, Product
from .serializers import OrganizationSerializer,ProductSerializer
from .filters import OrganizationFilter
from .permissions import IsAuthorOrReadOnly, IsOrganizationOrReadOnly
from review.models import OrganizationRating, OrganizationLike, ProductFavorite
from review.serializers import OrganizationRatingSerializer, ProductFavoriteSerializer


User = get_user_model()


class OrginizationViewSet(ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    filterset_class = OrganizationFilter


    def get_permissions(self):
        return [IsAuthorOrReadOnly()]
    

    @action(['POST'], detail=True)
    def rating(self, request, pk=None):
        if type(request.data) == QueryDict:
            request.data._mutable = True
        
        request.data.update({'organization': get_object_or_404(Organization, id=pk)})
        user = request.user
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


    def get_queryset(self):
        return Product.objects.filter(organization=self.kwargs['organization_pk'])


    def get_permissions(self):
        return [IsOrganizationOrReadOnly()]


    def create(self, request, organization_pk, *args, **kwargs):
        if type(request.data) == QueryDict:
            request.data._mutable = True
        
        request.data.update({'organization': organization_pk})

        return super().create(request, *args, **kwargs)
    

    def update(self, request, organization_pk, *args, **kwargs):
        if request.data.get('organization'):
            raise NotAcceptable(detail='Field "organization" not available for update')

        if type(request.data) == QueryDict:
            request.data._mutable = True
        
        request.data.update({'organization': organization_pk})

        return super().update(request, *args, **kwargs)
    

    @action(['PUT'], detail=True)
    def favorite(self, request, pk=None, *args, **kwargs):
        user_id = request.user.id
        user = get_object_or_404(User, id=user_id)
        product = get_object_or_404(Product, id=pk)

        if ProductFavorite.objects.filter(product=product, user=user).exists():
            ProductFavorite.objects.filter(product=product, user=user).delete()
        else:
            ProductFavorite.objects.create(product=product, user=user)

        return Response(status=201)


@swagger_auto_schema(
    manual_parameters=[
        openapi.Parameter('q', openapi.IN_QUERY, type=openapi.TYPE_STRING),
    ], method='GET'
)
@api_view(['GET'])
def search(request):
    q = request.query_params.get('q')

    if q:
        organizations = Organization.objects.filter(title__icontains=q)
        products = Product.objects.filter(title__icontains=q)
        organizations = OrganizationSerializer(organizations, many=True)
        products = ProductSerializer(products, many=True)
        result = organizations.data + products.data
    
        if result:
            paginated_result = PageNumberPagination().paginate_queryset(result, request)

            return Response(paginated_result, status=200)
    
    raise NotFound('По вашему запросу ничего не найдено.')
