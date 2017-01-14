'''
isort:skip_file
'''

from .routers import DefaultRouter

router = DefaultRouter(trailing_slash=False)

# Login / Register
from .social_auth.views import SocialAuthViewSet  # noqa

router.register(r'social-auth', SocialAuthViewSet, base_name='social-auth')
