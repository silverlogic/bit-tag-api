from django.conf import settings
from django.contrib.gis.db.models import PointField
from django.db import models
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _

from django_fsm import FSMField, transition
from model_utils import Choices
from push_notifications.models import APNSDevice

from apps.users.models import User


class Game(models.Model):
    Status = Choices(
        ('pending', _('Pending')),
        ('started', _('Started')),
    )

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='games')
    center_point = PointField(srid=4326)
    radius = models.FloatField()
    buy_in = models.DecimalField(max_digits=12, decimal_places=8)
    status = FSMField(choices=Status, default=Status.pending)

    @transition(status, source=Status.pending, target=Status.started)
    def start(self):
        pass


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

    @transition(status, source=Status.invited, target=Status.joined)
    def join(self):
        users = User.objects.filter(Q(games=self.game) | Q(participants__game=self.game))
        APNSDevice.objects.filter(user__in=users).send_message('participant_joined')

    @transition(status, source=Status.joined, target=Status.tagged)
    def tag(self, tagged_by):
        self.tagged_by = tagged_by
        users = User.objects.filter(Q(games=self.game) | Q(participants__game=self.game))
        APNSDevice.objects.filter(user__in=users).send_message('participant_tagged')
