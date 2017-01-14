from rest_framework import mixins, viewsets

from apps.games.models import Game

from .serializers import GameSerializer


class GamesViewSet(mixins.CreateModelMixin,
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
