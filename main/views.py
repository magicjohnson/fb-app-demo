# coding=utf-8
from django.views.generic import TemplateView

from allauth.account import views as allauth_views


class IndexView(TemplateView):
    template_name = 'main/index.html'


class LoginView(allauth_views.LoginView):
    template_name = 'main/login.html'
