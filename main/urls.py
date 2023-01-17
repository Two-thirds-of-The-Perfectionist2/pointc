from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrginizationViewSet, ProductViewSet

router = DefaultRouter()
router.register('organization', OrginizationViewSet)
router.register('product', ProductViewSet)

urlpatterns =[
    path('', include(router.urls)),
]
