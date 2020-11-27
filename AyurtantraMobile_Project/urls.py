"""AyurtantraMobile_Project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from rest_framework.schemas import get_schema_view
from rest_framework.documentation import include_docs_urls
from rest_framework.permissions import AllowAny

schema_view = get_schema_view(title='Mobile API')

urlpatterns = [
    path('app/admin/', admin.site.urls),
    path('app/api-auth/', include('rest_framework.urls')),
    path('app/rest-auth/', include('dj_rest_auth.urls')),
    path('app/rest-auth/registration/', include('dj_rest_auth.registration.urls')),
    path('app/accounts/', include('allauth.urls')), # all-auth's user management
    #path('accounts/', include('users.urls')), # user signup url when using Django's user management
    path('app/docs/', include_docs_urls(title='Mobile API', permission_classes=[AllowAny])),
    path('app/schema/', schema_view),
    #path('app/',include('pts_app.urls')),
    path('app/',include('patients.urls')),
    path('app/',include('dr_app.urls')),
    path('app/', include('django.contrib.auth.urls')), # Django's User management
    path('app/', include('homepage.urls')), #homepage
]
