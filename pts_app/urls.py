from django.urls import path

from .views import MyDoctor_API

urlpatterns = [
    path('my-doctors/',MyDoctor_API.as_view(), name='my-doctors-url'),
]