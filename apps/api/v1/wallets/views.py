from io import BytesIO

import qrcode
from push_notifications.models import APNSDevice
from rest_framework import mixins, viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response

from apps.wallets.models import Address, Transaction

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


class NotificationsViewSet(mixins.CreateModelMixin,
                           viewsets.GenericViewSet):
    def create(self, request, *args, **kwargs):
        data = request.data
        if data['type'] == 'wallet:addresses:new-payment':
            try:
                address = Address.objects.get(coinbase_id=data['data']['id'])
                Transaction.objects.get_or_create(
                    address=address,
                    amount=data['additional_data']['amount']['amount']
                )
                APNSDevice.objects.filter(user=address.user).send_message({'type': 'load_received'})
            except Address.objects.DoesNotExist:
                pass
        return Response({})
