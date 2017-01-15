from io import BytesIO

import qrcode
from push_notifications.models import APNSDevice
from rest_framework import mixins, renderers, status, viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response

from apps.base.coinbase import coinbase_client
from apps.wallets.models import Address, Transaction

from .serializers import AddressSerializer, SendMoneySerializer


class PngRenderer(renderers.BaseRenderer):
    media_type = 'image/png'
    format = 'png'
    charset = None
    render_style = 'binary'

    def render(self, data, media_type=None, renderer_context=None):
        return data


class AddressesViewSet(mixins.CreateModelMixin,
                       viewsets.GenericViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer

    @detail_route(methods=['GET'], renderer_classes=[PngRenderer])
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
        print(data)
        if data['type'] == 'wallet:addresses:new-payment':
            try:
                address = Address.objects.get(coinbase_id=data['data']['resource']['id'])
                Transaction.objects.get_or_create(
                    address=address,
                    amount=data['data']['amount']['amount']
                )
                APNSDevice.objects.get(user=address.user).send_message(None, content_available=True, extra={'type': 'load_received'})
            except Address.DoesNotExist:
                pass
        return Response({})


class SendMoneyViewSet(mixins.CreateModelMixin,
                       viewsets.GenericViewSet):
    serializer_class = SendMoneySerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        coinbase_client.send_money(
            request.user.coinbase_account_id,
            {
                'to': serializer.data['address'],
                'amount': str(serializer.data['amount']),
                'currency': 'BTC'
            }
        )
        return Response({}, status=status.HTTP_201_CREATED)
