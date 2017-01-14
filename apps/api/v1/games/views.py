from rest_framework import mixins, viewsets

from apps.games.models import Game, Participant

from .serializers import GameSerializer, ParticipantSerializer


class GamesViewSet(mixins.CreateModelMixin,
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer


class ParticipantsViewSet(mixins.CreateModelMixin,
                          mixins.ListModelMixin,
                          viewsets.GenericViewSet):
    queryset = Participant.objects.all()
    serializer_class = ParticipantSerializer
