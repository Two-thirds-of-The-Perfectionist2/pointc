"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static
from drf_yasg import openapi
from drf_yasg.views import get_schema_view


swagger_view = get_schema_view(
    openapi.Info(
        title='POINTC API',
        default_version = 'v1',
        description='pointc API'
    ),
    public=True
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('docs/', swagger_view.with_ui('swagger', cache_timeout=0)),
    path('users/', include('book.urls')),
    path('chat/', include('chat.urls')),
    path('', include('main.urls')),
    path('', include('review.urls')),
    path('', include('shop.urls')),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
