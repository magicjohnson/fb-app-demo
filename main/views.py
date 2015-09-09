# coding=utf-8
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from allauth.account import views as allauth_views


class IndexView(TemplateView):
    template_name = 'main/index.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(IndexView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        self._add_profile_image_to_context(context)
        return context

    def _add_profile_image_to_context(self, context):
        try:
            fb_account = self.request.user.socialaccount_set.get(provider='facebook')
            context.update({
                'profile_image': fb_account.get_avatar_url()
            })
        except ObjectDoesNotExist:
            pass


class LoginView(allauth_views.LoginView):
    template_name = 'main/login.html'
