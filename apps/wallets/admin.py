from django.contrib import admin

from .models import Address, Transaction


class AddressAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'coinbase_id', 'address',)


class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'address', 'amount',)


admin.site.register(Address, AddressAdmin)
admin.site.register(Transaction, TransactionAdmin)
