# coding=utf-8
import logging
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseBadRequest
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, View

from allauth.account import views as allauth_views
from allauth.socialaccount.models import SocialApp

from main.utils import parse_signed_request

User = get_user_model()
logger = logging.getLogger('logger')


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


class DeauthCallbackView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(DeauthCallbackView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        try:
            fb_app = SocialApp.objects.get_current('facebook')
            logger.debug(request.POST['signed_request'])
            data = parse_signed_request(request.POST['signed_request'], fb_app.client_id)
            user = User.objects.get(facebook_id=data['user_id'])

            user.is_active = False
            user.save()
            return HttpResponse()

        except Exception:
            return HttpResponseBadRequest()
