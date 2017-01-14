from rest_framework import filters, mixins, response, viewsets
from rest_framework.decorators import detail_route

from apps.games.models import Game, Participant

from .serializers import GameSerializer, ParticipantSerializer


class GamesViewSet(mixins.CreateModelMixin,
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer

    @detail_route(methods=['POST'])
    def start(self, request, pk=None, *args, **kwargs):
        game = self.get_object()
        game.start()
        game.save()
        return response.Response({})


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

    @detail_route(methods=['POST'])
    def tag(self, request, pk=None, *args, **kwargs):
        participant = self.get_object()
        participant.tag(tagged_by=Participant.objects.get(game=participant.game, user=request.user))
        participant.save()
        return response.Response({})
