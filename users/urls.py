from django.urls import path

from .views import email_verified_view

urlpatterns = [
    #path('signup/', SignupPageView.as_view(), name='signup'),
    path('',email_verified_view,name='password_reset_confirm')
]