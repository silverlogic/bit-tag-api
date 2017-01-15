from django.contrib.gis.db.models import PointField
from django.db import models
from django.utils.translation import ugettext_lazy as _

from model_utils import Choices


class PointOfInterest(models.Model):
    Type = Choices(
        ('atm', _('ATM')),
        ('merchant', _('Merchant')),
    )

    name = models.CharField(max_length=100, blank=True)
    type = models.CharField(max_length=20, choices=Type)
    point = PointField()
