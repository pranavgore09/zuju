from django.contrib import admin

from tournaments.models import Tournament


# Register your models here.
@admin.register(Tournament)
class TournamentAdmin(admin.ModelAdmin):
    list_display = [
        'uuid',
        'title',
        'start_at',
        'end_at',
    ]
