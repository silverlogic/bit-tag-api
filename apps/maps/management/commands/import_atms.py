from django.core.management.base import BaseCommand
from django.contrib.gis.geos import Point

import requests

from ...models import PointOfInterest


class Command(BaseCommand):
    help = 'Import atms from coinatmradar'

    def handle(self, *args, **options):
        for index, atm in requests.get('https://coinatmradar.com/api/locations/2010-01-01/').json().items():
            PointOfInterest.objects.create(
                type=PointOfInterest.Type.atm,
                point=Point(float(atm['long']), float(atm['lat']))
            )
