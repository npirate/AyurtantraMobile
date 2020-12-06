from django.urls import path, re_path, path
from .views import Any_SP_API

urlpatterns =[
    re_path(r'^(?P<id>\d+)/',Any_SP_API.as_view(),name='any-sp-api-url'),
]