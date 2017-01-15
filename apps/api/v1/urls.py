'''
isort:skip_file
'''

from .routers import DefaultRouter

router = DefaultRouter(trailing_slash=False)

# Login / Register
from .social_auth.views import SocialAuthViewSet  # noqa

router.register(r'social-auth', SocialAuthViewSet, base_name='social-auth')

# Users
from .users.views import UsersViewSet  # noqa

router.register(r'users', UsersViewSet, base_name='users')

# Games
from .games.views import GamesViewSet, ParticipantsViewSet  # noqa

router.register(r'games', GamesViewSet, base_name='games')
router.register(r'participants', ParticipantsViewSet, base_name='participants')

# Maps
from .maps.views import PointsOfInterestViewSet  # noqa

router.register(r'points-of-interest', PointsOfInterestViewSet, base_name='points-of-interest')

# Wallets
from .wallets.views import AddressesViewSet, NotificationsViewSet, SendMoneyViewSet  # noqa

router.register(r'addresses', AddressesViewSet, base_name='addresses')
router.register(r'coinbase-notifications', NotificationsViewSet, base_name='coinbase-notifications')
router.register(r'send-money', SendMoneyViewSet, base_name='send-money')
