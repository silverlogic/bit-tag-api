from django.contrib import admin

from .models import Game, Participant


class GameAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', 'center_point', 'radius', 'buy_in', 'status',)


class ParticipantAdmin(admin.ModelAdmin):
    list_display = ('id', 'game', 'user', 'status',)


admin.site.register(Game, GameAdmin)
admin.site.register(Participant, ParticipantAdmin)
