# coding=utf-8
import dj_database_url

try:
    from fb_app.settings.base import *
except ImportError:
    pass

DATABASES['default'] = dj_database_url.config()

EMAIL_BACKEND = 'django.core.mail.backends.dummy.EmailBackend'




