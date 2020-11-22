from django.urls import path
from .views import Search_Shloka_API

urlpatterns =[
    path('search-shloka/',Search_Shloka_API.as_view(),name='search-shloka-url'),
]