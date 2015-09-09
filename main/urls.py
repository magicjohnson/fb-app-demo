# coding=utf-8
from django.conf.urls import url

from main import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^accounts/login/$', views.LoginView.as_view(), name='login'),
    url(r'^accounts/facebook/deauth/$', views.DeauthCallbackView.as_view(), name='deauth_callback'),
]

