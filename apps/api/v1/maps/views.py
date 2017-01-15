import re

from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point

from rest_framework import mixins, viewsets

from apps.maps.models import PointOfInterest

from .serializers import PointOfInterestSerializer


class PointsOfInterestViewSet(mixins.ListModelMixin,
                              viewsets.GenericViewSet):
    queryset = PointOfInterest.objects.all()
    serializer_class = PointOfInterestSerializer

    def filter_queryset(self, qs):
        point = self.request.query_params.get('point', None)
        if point:
            if re.match(r'-?[\d.]+,-?[\d.]+', point):
                y, x = point.split(',')
                point = Point(float(x), float(y), srid=4326)
                qs = qs.annotate(distance=Distance('point', point)).order_by('distance')
        return qs
