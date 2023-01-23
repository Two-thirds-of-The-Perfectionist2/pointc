from django.http.request import QueryDict
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.decorators import api_view

from .tasks import send_confirmation_code
from .models import Delivery, Cart
from .serializers import DeliverySerializer, CartSerializer, DeliveryManSerializer


User = get_user_model()


class DeliveryViewSet(viewsets.ViewSet):
    
    def get_permissions(self):
        return [IsAuthenticatedOrReadOnly()]


    def create(self, request):
        ser = DeliverySerializer(data=request.data, context={'request': request})
        ser.is_valid(raise_exception=True)
        ser.save()
        send_confirmation_code.delay(ser.instance.customer.email, ser.instance.activation_code)
        return Response(status=201)


    def partial_update(self, request, pk=None):
        DELIVERY_AMOUNT = 100
        if type(request.data) == QueryDict:
            request.data._mutable = True

        delivery = get_object_or_404(Delivery, id=pk)
        request.data.update({'deliveryman': request.user.id})
        ser = DeliveryManSerializer(instance=delivery, data=request.data, partial=True, context={'request': request})
        ser.is_valid(raise_exception=True)

        amount = delivery.amount
        customer = delivery.customer
        if customer.balance >= amount:
            customer.balance -= amount
            customer.save()
            request.user.balance += DELIVERY_AMOUNT
            request.user.save()
            if not delivery.carts.exists():
                return Response('There is nothing in the cart', status=400)
            org_user = delivery.carts.first().product.organization.user
            org_user.balance += (amount - DELIVERY_AMOUNT)
            org_user.save()
            ser.save()
            return Response(status=201)
        else:
            return Response('Not enough money on the balance', status=400)


    def list(self, request):
        queryset = Delivery.objects.filter(deliveryman=None)
        ser = DeliverySerializer(queryset, many=True)

        return Response(ser.data)


class CartViewSet(viewsets.ViewSet):

    def get_queryset(self):
        return Cart.objects.filter(delivery=self.kwargs['delivery_pk'])


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
    delivery.activation_code = None
    delivery.save()

    return Response('Exellent, The order is confirmed!', status=200)