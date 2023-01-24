from django.http.request import QueryDict
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.decorators import api_view
from rest_framework.exceptions import NotAcceptable
from drf_yasg.utils import swagger_auto_schema

from .tasks import send_confirmation_code
from .models import Delivery, Cart
from .serializers import DeliverySerializer, CartSerializer, DeliveryManSerializer


User = get_user_model()


class DeliveryViewSet(viewsets.ViewSet):
    
    def get_permissions(self):
        return [IsAuthenticatedOrReadOnly()]


    @swagger_auto_schema(request_body=DeliverySerializer())
    def create(self, request):
        ser = DeliverySerializer(data=request.data, context={'request': request})
        ser.is_valid(raise_exception=True)
        ser.save()
        send_confirmation_code.delay(ser.instance.customer.email, ser.instance.activation_code)
        return Response(status=201)


    def partial_update(self, request, pk=None):
        delivery = get_object_or_404(Delivery, id=pk)
        
        if delivery.activation_code or delivery.deliveryman:
            raise NotAcceptable()

        if type(request.data) == QueryDict:
            request.data._mutable = True

        request.data.update({'deliveryman': request.user.id})
        ser = DeliveryManSerializer(instance=delivery, data=request.data, partial=True, context={'request': request})
        ser.is_valid(raise_exception=True)
        org_user = delivery.carts.first().product.organization.user
        org_user.balance += delivery.price.get('products')
        org_user.save()
        request.user.balance += delivery.price.get('delivery')
        request.user.save()
        ser.save()

        return Response(status=201)


    def list(self, request):
        queryset = Delivery.objects.filter(activation_code=None).order_by('deliveryman')
        ser = DeliverySerializer(queryset, many=True, context={'request': request})

        return Response(ser.data)


class CartViewSet(viewsets.ViewSet):

    def get_queryset(self):
        return Cart.objects.filter(delivery=self.kwargs['delivery_pk'])


    @swagger_auto_schema(request_body=CartSerializer())
    def create(self, request, delivery_pk, *args, **kwargs):
        if type(request.data) == QueryDict:
            request.data._mutable = True

        request.data.update({'delivery': get_object_or_404(Delivery, id=delivery_pk)})
        ser = CartSerializer(data=request.data, context={'request': request})
        ser.is_valid(raise_exception=True)
        ser.save()

        return Response(status=201)


@api_view(['GET'])
def activate_view(request, activation_code):
    delivery = get_object_or_404(Delivery, activation_code=activation_code)
    amount = round(sum(delivery.price.values()), 2)
    customer = delivery.customer

    if customer.balance >= amount:
        customer.balance -= amount
        customer.save()    
        delivery.activation_code = None
        delivery.save()

        return Response('Excellent, The order is confirmed!', status=200)
    else:
        return Response('Not enough money on the balance', status=400)
