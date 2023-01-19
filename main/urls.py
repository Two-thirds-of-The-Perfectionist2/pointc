from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedSimpleRouter

from .views import OrginizationViewSet, ProductViewSet, search


router = DefaultRouter()
router.register('organizations', OrginizationViewSet)
product_router = NestedSimpleRouter(router, 'organizations', lookup='organization')
product_router.register('products', ProductViewSet)

urlpatterns =[
    path('', include(router.urls)),
    path('', include(product_router.urls)),
    path('search/', search)
]
