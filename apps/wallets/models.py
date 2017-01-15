from django.conf import settings
from django.db import models


class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='addresses', on_delete=models.CASCADE)
    coinbase_id = models.CharField(max_length=100)
    address = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.coinbase_id} - {self.address}'


class Transaction(models.Model):
    address = models.ForeignKey('Address', related_name='transactions', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=8)
    status = models.CharField(max_length=50)
