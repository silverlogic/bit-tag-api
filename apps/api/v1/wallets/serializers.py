from rest_framework import serializers

from apps.base.coinbase import coinbase_client
from apps.wallets.models import Address

from ...serializers import ModelSerializer


class AddressSerializer(ModelSerializer):
    class Meta:
        model = Address
        fields = ('id', 'user', 'address',)
        read_only_fields = ('user', 'address',)

    def create(self, validated_data):
        user = self.context['request'].user
        coinbase_address = coinbase_client.create_address(user.coinbase_account_id)
        validated_data['user'] = user
        validated_data['coinbase_id'] = coinbase_address.id
        validated_data['address'] = coinbase_address.address
        return super().create(validated_data)


class SendMoneySerializer(serializers.Serializer):
    address = serializers.CharField()
    amount = serializers.DecimalField(max_digits=12, decimal_places=8)
