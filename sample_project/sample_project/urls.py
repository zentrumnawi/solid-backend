"""sample_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import include, path
from drf_spectacular.views import SpectacularSwaggerView, SpectacularAPIView, SpectacularRedocView

import solid_backend

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("solid_backend.urls")),
    path("", include("api_docs.api_docs"), name="api_docs"),
    # YOUR PATTERNS
    path(r'api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path(r'api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'),
         name='swagger-ui'),
    path(r'api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'),
         name='redoc'),
]
