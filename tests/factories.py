from decimal import Decimal

from django.contrib.gis.geos import Point

import factory


class UserFactory(factory.DjangoModelFactory):
    email = factory.Faker('email')
    password = factory.PostGenerationMethodCall('set_password', 'default')

    class Meta:
        model = 'users.User'


class GameFactory(factory.DjangoModelFactory):
    owner = factory.SubFactory('tests.factories.UserFactory')
    center_point = Point(0, 0)
    radius = 1
    buy_in = Decimal('0.00000010')

    class Meta:
        model = 'games.Game'
