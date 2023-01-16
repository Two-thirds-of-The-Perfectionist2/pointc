from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrginizationCardViewSet, ProductsViewSet

router = DefaultRouter()
router.register('organization', OrginizationCardViewSet)
router.register('products', ProductsViewSet)

urlpatterns =[
    path('', include(router.urls)),
]
