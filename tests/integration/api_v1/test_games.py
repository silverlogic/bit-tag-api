import pytest

from apps.games.models import Game

import tests.factories as f
import tests.helpers as h
from tests.mixins import ApiMixin

pytestmark = pytest.mark.django_db


class TestGamesCreate(ApiMixin):
    view_name = 'games-list'

    @pytest.fixture
    def data(self):
        return {
            "center_point": {
                "type": "Point",
                "coordinates": [
                    22.8515625,
                    17.764892578125
                ]
            },
            "radius": 3.5,
            "buy_in": "0.00000010",
            "status": "pending"
        }

    def test_user_can_create(self, user_client, data):
        r = user_client.post(self.reverse(), data)
        h.responseCreated(r)


class TestGamesStart(ApiMixin):
    view_name = 'games-start'

    def test_user_can_start_game(self, user_client):
        game = f.GameFactory()
        r = user_client.post(self.reverse(kwargs={'pk': game.pk}))
        h.responseOk(r)
        game.refresh_from_db()
        assert game.status == Game.Status.started
