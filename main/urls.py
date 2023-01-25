from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedSimpleRouter

from .views import OrganizationViewSet, ProductViewSet, search, recommendation, support_bot


router = DefaultRouter()
router.register('organizations', OrganizationViewSet)
product_router = NestedSimpleRouter(router, 'organizations', lookup='organization')
product_router.register('products', ProductViewSet)

urlpatterns =[
    path('', include(router.urls)),
    path('', include(product_router.urls)),
    path('search/', search),
    path('recommendations/', recommendation),
    path('support-bot/', support_bot),
]
