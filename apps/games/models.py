from decimal import Decimal

from django.conf import settings
from django.contrib.gis.db.models import PointField
from django.db import models
from django.utils.translation import ugettext_lazy as _

from django_fsm import FSMField, transition
from model_utils import Choices
from push_notifications.models import APNSDevice

from apps.users.models import User


class Game(models.Model):
    Status = Choices(
        ('pending', _('Pending')),
        ('started', _('Started')),
        ('ended', _('Ended')),
    )

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='games')
    center_point = PointField(srid=4326)
    radius = models.FloatField()
    buy_in = models.DecimalField(max_digits=12, decimal_places=8)
    status = FSMField(choices=Status, default=Status.pending)

    @transition(status, source=Status.pending, target=Status.started)
    def start(self):
        users = User.objects.filter(participant__game=self)
        APNSDevice.objects.filter(user__in=users).send_message(None, content_available=True, extra={'type': 'game_started'})

    @transition(status, source=Status.started, target=Status.ended)
    def end(self):
        users = User.objects.filter(participant__game=self)
        APNSDevice.objects.filter(user__in=users).send_message(None, content_available=True, extra={'type': 'game_ended'})


class Participant(models.Model):
    Status = Choices(
        ('invited', _('Invited')),
        ('joined', _('Joined')),
        ('tagged', _('Tagged')),
    )

    game = models.ForeignKey('Game', related_name='participants', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    status = FSMField(choices=Status, default=Status.invited)
    tagged_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, related_name='tagged', on_delete=models.CASCADE)

    @property
    def btc_earned(self):
        participant_count = self.game.participants.count()

        pool = self.game.buy_in * participant_count
        winner_pool = Decimal(20) * pool / Decimal(100)
        remaining_pool = pool - winner_pool
        tag_amount = remaining_pool / (participant_count - 1)

        earned = Decimal(0)
        earned = tag_amount * Participant.objects.filter(game=self.game, tagged_by=self.user).count()

        if self.game.status == Game.Status.ended and self.status != Participant.Status.tagged:
            earned += winner_pool

        return earned

    @transition(status, source=Status.invited, target=Status.joined)
    def join(self):
        users = User.objects.filter(participant__game=self.game)
        APNSDevice.objects.filter(user__in=users).send_message(None, content_available=True, extra={'type': 'participant_joined'})

    @transition(status, source=Status.joined, target=Status.tagged)
    def tag(self, tagged_by):
        self.tagged_by = tagged_by
        users = User.objects.filter(participant__game=self.game)
        APNSDevice.objects.filter(user__in=users).send_message(None, content_available=True, extra={'type': 'participant_tagged'})
        if Participant.objects.exclude(status=self.Status.tagged).count() == 1:
            self.game.end()
            self.game.save()
