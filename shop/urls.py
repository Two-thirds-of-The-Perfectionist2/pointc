from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedSimpleRouter

from .views import CartViewSet, DeliveryViewSet


router = DefaultRouter()
router.register('deliveries', DeliveryViewSet, basename='delivery')

cart_router = NestedSimpleRouter(router, 'deliveries', lookup='delivery')
cart_router.register('carts', CartViewSet, basename='cart')


urlpatterns = [
    path('', include(router.urls)),
    path('', include(cart_router.urls)),
]