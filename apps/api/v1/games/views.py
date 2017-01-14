from rest_framework import mixins, viewsets, filters, response
from rest_framework.decorators import detail_route

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
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('game', 'user', 'status',)

    @detail_route(methods=['POST'])
    def join(self, request, pk=None, *args, **kwargs):
        participant = self.get_object()
        participant.join()
        participant.save()
        return response.Response({})
