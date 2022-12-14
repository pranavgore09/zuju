import random
from datetime import datetime, timedelta
from typing import List, Tuple

from django.conf import settings
from django.db.models.query_utils import Q
from django.utils import timezone

from fixtures.models import Fixture
from fixtures.serializers import FixtureSerializer
from teams.models import Team

# from dateutil.relativedelta import relativedelta


def date_range(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        date = start_date + timedelta(n)
        date = date.replace(second=0, microsecond=0)
        yield date


class FixtureApi:

    @classmethod
    def get_or_create(cls, fixture_data) -> Tuple[Fixture, bool]:
        tournament = fixture_data['tournament']
        home_team = fixture_data['home_team']
        away_team = fixture_data['away_team']
        start_at = fixture_data['start_at']
        end_at = fixture_data['end_at']
        weekday = fixture_data['weekday']
        return Fixture.objects.get_or_create(
            tournament_id=tournament,
            home_team_id=home_team,
            away_team_id=away_team,
            start_at=start_at,
            end_at=end_at,
            weekday=weekday,
        )

    @classmethod
    def bulk_create(cls, *args, **kwargs) -> List[Fixture]:
        fixtures_per_day = kwargs.get('fixtures_per_day',
                                      settings.FIXTURES_PER_DAY)
        # ref: https://docs.python.org/3/library/datetime.html#datetime.datetime.weekday
        # Saturday=5, Sunday=6, Monday=0
        fixtures_on_weekday = settings.FIXTURES_ON_WEEKDAY

        tournament = kwargs['tournament']

        fixture_data = {
            'tournament': tournament.id,
        }

        available_team_ids = list(
            Team.objects.all().values_list(
                'id',
                flat=True,
            ), )
        fixtures = []
        start_date = tournament.start_at
        end_date = tournament.end_at
        for single_date in date_range(start_date, end_date):
            if single_date.weekday() in fixtures_on_weekday:
                temp_date = single_date
                fixture_start_at = temp_date.replace(hour=16)
                fixture_end_at = fixture_start_at + timedelta(minutes=90)
                for _ in range(fixtures_per_day):
                    teams = random.sample(available_team_ids, 2)
                    fixture_data['home_team'] = teams[0]
                    fixture_data['away_team'] = teams[1]
                    fixture_data['start_at'] = fixture_start_at
                    fixture_data['end_at'] = fixture_end_at
                    fixture_data['weekday'] = fixture_start_at.weekday()
                    team, _ = FixtureApi.get_or_create(fixture_data)
                    fixtures.append(team)
        return fixtures
