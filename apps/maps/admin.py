from django.contrib import admin

from .models import PointOfInterest


class PointOfInterestAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'type',)


admin.site.register(PointOfInterest, PointOfInterestAdmin)
