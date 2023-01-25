from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.http.request import QueryDict
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.exceptions import NotAcceptable, NotFound, NotAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

from .models import Organization, Product
from .serializers import OrganizationSerializer,ProductSerializer, SubscriptionSerializer
from .filters import OrganizationFilter    
from .permissions import IsAuthorOrReadOnly, IsOrganizationOrReadOnly
from review.models import OrganizationRating, OrganizationLike, ProductFavorite, Subscription
from review.serializers import OrganizationRatingSerializer
from shop.models import Delivery
from shop.serializers import DeliverySerializer, CartSerializer


User = get_user_model()


class OrganizationViewSet(ModelViewSet):
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
    

    @action(['POST'], detail=True)
    def subscribe(self, request, pk=None):
        if not request.user.is_authenticated:
            raise NotAuthenticated

        user_id = request.user.id
        user = get_object_or_404(User, id=user_id)
        subscribe = get_object_or_404(Organization, id=pk)
        

        if Subscription.objects.filter(subscribe=subscribe, user=user).exists():
            Subscription.objects.filter(subscribe=subscribe, user=user).delete()
        else:
            Subscription.objects.create(subscribe=subscribe, user=user)

        return Response(status=201)



class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsOrganizationOrReadOnly]
    
    @method_decorator(cache_page(60 * 1))
    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('q', openapi.IN_QUERY, type=openapi.TYPE_STRING),
    ])
    def list(self, request, *args, **kwargs):
        q = request.query_params.get('q')

        if q:
            products = Product.objects.filter(title__icontains=q)
            result = ProductSerializer(products, many=True).data
            paginated_result = PageNumberPagination().paginate_queryset(result, request)

            return Response(paginated_result, status=200)
        
        return super().list(request, *args, **kwargs)

    def get_queryset(self):
        return Product.objects.filter(organization=self.kwargs['organization_pk'])


    def create(self, request, organization_pk, *args, **kwargs):
        self.check_permissions(request)
        self.check_object_permissions(request=request, obj=get_object_or_404(Organization, id=organization_pk))
        if type(request.data) == QueryDict:
            request.data._mutable = True
        
        request.data.update({'organization': organization_pk})

        return super().create(request, *args, **kwargs)
    

    def update(self, request, organization_pk, *args, **kwargs):

        self.check_permissions(request)
        self.check_object_permissions(request=request, obj=get_object_or_404(Organization, id=organization_pk))
        # if request.data.get('organization'):
            # raise NotAcceptable(detail='Field "organization" not available for update')
            
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
        openapi.Parameter('filter', openapi.IN_QUERY, type=openapi.TYPE_STRING),
    ], method='GET'
)
@api_view(['GET'])
def search(request):
    q = request.query_params.get('q')
    
    if not q:
        raise NotFound('Missing query parameters.')

    filter_ = request.query_params.get('filter')

    if not filter_:
        organizations = Organization.objects.filter(title__icontains=q)
        products = Product.objects.filter(title__icontains=q)
        organizations = OrganizationSerializer(organizations, many=True)
        products = ProductSerializer(products, many=True)
        result = organizations.data + products.data

    elif filter_ == 'organizations':
        organizations = Organization.objects.filter(title__icontains=q)
        organizations = OrganizationSerializer(organizations, many=True)
        result = organizations.data

    elif filter_ == 'products':
        products = Product.objects.filter(title__icontains=q)
        products = ProductSerializer(products, many=True)
        result = products.data

    else:
        raise NotFound('Invalid filter parameter.')

    if not result:
        raise NotFound('No results found for your query.')

    paginated_result = PageNumberPagination().paginate_queryset(result, request)

    return Response(paginated_result, status=200)


@api_view(['GET'])
def recommendation(request):
    if not request.user.is_authenticated:
        raise NotAuthenticated
    
    deliveries = Delivery.objects.filter(customer=request.user.id)
    carts = [j.all() for j in [i.carts for i in deliveries]]
    products = [i.first().product for i in carts]
    organizations = [i.organization for i in products]
    tags = [i.tag for i in organizations]
    categories = [i.category for i in organizations]
    rec = tags + categories
    
    organization = [i for i in Organization.objects.all() if i.category in rec or i.tag in rec]
    ser = OrganizationSerializer(organization, many=True)

    return Response(ser.data, status=200)


@swagger_auto_schema(
    manual_parameters=[
        openapi.Parameter('q', openapi.IN_QUERY, type=openapi.TYPE_STRING),
    ], method='GET'
)
@api_view(['GET'])
def support_bot(request):
    q = request.query_params.get('q')
    
    questions = ('question 1', 'question 2', 'question 3', 'question 4')
    answers = ('answer 1', 'answer 2', 'answer 3', 'answer 4')

    if not q:
        return Response(questions)
    
    try:
        answer = answers[int(q)-1]
    except (ValueError, IndexError):
        return Response('Параметр введен неверно.', status=400)

    return Response(answer, status=200)
