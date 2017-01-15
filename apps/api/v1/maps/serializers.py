from apps.maps.models import PointOfInterest

from ...serializers import ModelSerializer


class PointOfInterestSerializer(ModelSerializer):
    class Meta:
        model = PointOfInterest
        fields = ('id', 'name', 'type', 'point',)
