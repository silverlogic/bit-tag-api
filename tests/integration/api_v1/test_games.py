import pytest

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
