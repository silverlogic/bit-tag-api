import pytest

from apps.games.models import Participant

import tests.factories as f
import tests.helpers as h
from tests.mixins import ApiMixin

pytestmark = pytest.mark.django_db


class TestParticipantsCreate(ApiMixin):
    view_name = 'participants-list'

    @pytest.fixture
    def data(self):
        return {
            'game': f.GameFactory().pk,
            'user': f.UserFactory().pk,
        }

    def test_user_can_create(self, user_client, data):
        r = user_client.post(self.reverse(), data)
        h.responseCreated(r)


class TestParticipantsJoin(ApiMixin):
    view_name = 'participants-join'

    def test_user_can_join(self, user_client):
        participant = f.ParticipantFactory()
        r = user_client.post(self.reverse(kwargs={'pk': participant.pk}))
        h.responseOk(r)
        participant.refresh_from_db()
        assert participant.status == Participant.Status.joined
