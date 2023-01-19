from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import *


urlpatterns = [
    path('register/', RegisterUserView.as_view()),
    path('activate/<str:activation_code>/', activate_view),
    path('login/', TokenObtainPairView.as_view()),
    path('login/refresh/', TokenRefreshView.as_view()),
    path('delete/<int:id>/', delete_user),
    path('<int:id>/', details_user),
    path('<int:id>/rating/', rating),
    path('forgot/', forgot_password),
    path('accept/<str:activation_code>/', new_password_post),
    path('balance_topup/', add_balance),
]