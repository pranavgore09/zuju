from django.db import models

from teams.models import Team
from tournaments.models import Tournament
from z_common.models import BaseDateTimeUUIDModel


class Fixture(BaseDateTimeUUIDModel):

    tournament = models.ForeignKey(
        Tournament,
        on_delete=models.PROTECT,
        null=False,
    )

    # Handle in application layer that teams are different
    home_team = models.ForeignKey(
        Team,
        on_delete=models.PROTECT,
        related_name='home',
        null=False,
    )
    away_team = models.ForeignKey(
        Team,
        on_delete=models.PROTECT,
        related_name='away',
        null=False,
    )
    start_at = models.DateTimeField(db_index=True)
    end_at = models.DateTimeField()

    # Fixture's current state
    STATE_CONFIRMED = 'confirmed'
    STATE_CANCELLED = 'cancelled'
    STATE_LIVE = 'live'
    STATE_FT = 'full_time'
    STATE_DELAYED = 'delayed'

    STATE_CHOICES = (
        (STATE_CONFIRMED, 'Confirmed'),
        (STATE_CANCELLED, 'Cancelled'),
        (STATE_LIVE, 'Live'),
        (STATE_FT, 'Full Time'),
        (STATE_DELAYED, 'Delayed'),
    )
    state = models.CharField(max_length=15,
                             choices=STATE_CHOICES,
                             default=STATE_CONFIRMED,
                             db_index=True)

    # can be used as away_conceded
    home_score = models.IntegerField(default=-1)

    # can be used as home_conceded
    away_score = models.IntegerField(default=-1)

    DAY_M = 0
    DAY_TU = 1
    DAY_W = 2
    DAY_TH = 3
    DAY_F = 4
    DAY_SA = 5
    DAY_SU = 6

    DAY_NAMES = (
        (DAY_M, 'Monday'),
        (DAY_TU, 'Tuesday'),
        (DAY_W, 'Wednesday'),
        (DAY_TH, 'Thursday'),
        (DAY_F, 'Friday'),
        (DAY_SA, 'Saturday'),
        (DAY_SU, 'Sunday'),
    )
    # fixture's start day in text
    weekday = models.IntegerField(
        choices=DAY_NAMES,
        default=DAY_SU,
    )

    def __str__(self) -> str:
        return f'Fixture:{self.home_team.name}<>{self.away_team.name}'
