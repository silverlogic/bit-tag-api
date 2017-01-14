from .base import *  # noqa

DEBUG = False
SECRET_KEY = env('SECRET_KEY')

# Email
DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL')
DJMAIL_REAL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Static / Media Files
MEDIA_ROOT = str(BASE_DIR.parent / 'media')
MEDIA_URL = '/media/'
STATIC_ROOT = str(BASE_DIR.parent / 'static')
STATIC_URL = '/static/'
