from expander import ExpanderSerializerMixin
from push_notifications.models import APNSDevice
from rest_framework import serializers

from apps.games.models import Game, Participant
from apps.users.models import User

from ...serializers import ModelSerializer
from ..users.serializers import UserSerializer


class GameSerializer(ModelSerializer):
    class Meta:
        model = Game
        fields = ('id', 'owner', 'center_point', 'radius', 'buy_in', 'status',)
        read_only_fields = ('owner', 'status',)

    def create(self, validated_data):
        validated_data['owner'] = self.context['request'].user
        game = super().create(validated_data)
        Participant.objects.create(
            game=game,
            user=validated_data['owner'],
            status=Participant.Status.joined
        )
        return game


class ParticipantSerializer(ExpanderSerializerMixin, ModelSerializer):
    btc_earned = serializers.DecimalField(max_digits=12, decimal_places=8, read_only=True)

    class Meta:
        model = Participant
        fields = ('id', 'game', 'user', 'status', 'btc_earned',)
        read_only_fields = ('status',)
        expandable_fields = {
            'user': UserSerializer
        }

    def create(self, validated_data):
        participant = super().create(validated_data)
        APNSDevice.objects.filter(user=validated_data['user']).send_message(None, content_available=True, extra={'type': 'you_invited'})

        users = User.objects.filter(participant__game=self.game).exclude(pk=validated_data['user'].pk)
        APNSDevice.objects.filter(user__in=users).send_message(None, content_available=True, extra={'type': 'participant_invited'})

        return participant
