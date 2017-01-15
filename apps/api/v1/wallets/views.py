from io import BytesIO

import qrcode
from rest_framework import mixins, viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response

from apps.wallets.models import Address

from .serializers import AddressSerializer


class AddressesViewSet(mixins.CreateModelMixin,
                       viewsets.GenericViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer

    @detail_route(methods=['GET'])
    def qrcode(self, request, pk=None, *args, **kwargs):
        address = self.get_object()
        img = qrcode.make(address.address)
        output = BytesIO()
        img.save(output)
        return Response(output.getvalue())
