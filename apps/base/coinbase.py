from django.conf import settings

from coinbase.wallet.client import Client

coinbase_client = Client(settings.COINBASE_API_KEY, settings.COINBASE_API_SECRET)
