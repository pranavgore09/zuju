from django.contrib import admin

from tournaments.models import Tournament
from z_common.admin import BaseUUIDAdmin


# Register your models here.
@admin.register(Tournament)
class TournamentAdmin(BaseUUIDAdmin):
    list_display = [
        'uuid',
        'title',
        'start_at',
        'end_at',
    ]

    search_fields = [
        'title',
    ]
