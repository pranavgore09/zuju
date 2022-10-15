from django.contrib import admin

from fixtures.models import Fixture
from z_common.admin import TeamSearch, TournamentSearch

# Register your models here.


@admin.register(Fixture)
class FixtureAdmin(admin.ModelAdmin):
    list_display = [
        'uuid',
        'tournament',
        'state',
        'home_team',
        'away_team',
        'start_at',
        'end_at',
    ]

    list_filter = (
        TournamentSearch,
        TeamSearch,
        'state',
        'start_at',
        'end_at',
        'created_at',
        'modified_at',
    )

    raw_id_fields = [
        'tournament',
        'home_team',
        'away_team',
    ]
