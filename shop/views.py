from django.http.request import QueryDict
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import serializers

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

        return Response(status=201)


    def partial_update(self, request, pk=None):
        # if not request.data.get('deliveryman'):
        #     raise serializers.ValidationError()

        if type(request.data) == QueryDict:
            request.data._mutable = True

        delivery = get_object_or_404(Delivery, id=pk)
        request.data.update({'deliveryman': request.user.id})
        ser = DeliveryManSerializer(instance=delivery, data=request.data, partial=True, context={'request': request})
        ser.is_valid(raise_exception=True)
        ser.save()

        return Response(status=201)


    def list(self, request):
        # queryset = Delivery.objects.filter(deliveryman=None)
        queryset = Delivery.objects.all()
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
