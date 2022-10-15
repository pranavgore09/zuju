from django.contrib import admin

from teams.models import Team
from z_common.admin import BaseUUIDAdmin


# Register your models here.
@admin.register(Team)
class TeamAdmin(BaseUUIDAdmin):
    list_display = [
        'uuid',
        'name',
    ]

    search_fields = [
        'name',
    ]
