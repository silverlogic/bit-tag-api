from apps.games.models import Game, Participant

from ...serializers import ModelSerializer


class GameSerializer(ModelSerializer):
    class Meta:
        model = Game
        fields = ('id', 'owner', 'center_point', 'radius', 'buy_in', 'status',)
        read_only_fields = ('owner', 'status',)

    def create(self, validated_data):
        validated_data['owner'] = self.context['request'].user
        return super().create(validated_data)


class ParticipantSerializer(ModelSerializer):
    class Meta:
        model = Participant
        fields = ('id', 'game', 'user', 'status',)
        read_only_fields = ('status',)
