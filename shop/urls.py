from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedSimpleRouter

from .views import CartViewSet, DeliveryViewSet, activate_view, order_done


router = DefaultRouter()
router.register('deliveries', DeliveryViewSet, basename='delivery')

cart_router = NestedSimpleRouter(router, 'deliveries', lookup='delivery')
cart_router.register('carts', CartViewSet, basename='cart')


urlpatterns = [
    path('', include(router.urls)),
    path('', include(cart_router.urls)),
    path('deliveries/accept/<str:activation_code>/', activate_view),
    path('deliveries/done/<int:id>/', order_done),
]