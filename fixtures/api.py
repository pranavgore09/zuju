import random
from datetime import date, datetime, timedelta
from typing import List, Tuple

from django.db.models.query_utils import Q
from django.utils import timezone
from rest_framework import serializers

from fixtures.models import Fixture
from teams.models import Team

# from dateutil.relativedelta import relativedelta


def date_range(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)


class FixtureSerializer(serializers.ModelSerializer):

    class Meta:
        model = Fixture
        fields = (
            'uuid',
            'tournament',
            'home_team',
            'away_team',
            'start_at',
            'end_at',
        )
        read_only_fields = (
            'uuid',
            'tournament',
            'home_team',
            'away_team',
            'start_at',
            'end_at',
        )


class FixtureApi:

    @classmethod
    def get_or_create(cls, fixture_data) -> Tuple[Fixture, bool]:
        tournament = fixture_data['tournament']
        home_team = fixture_data['home_team']
        away_team = fixture_data['away_team']
        start_at = fixture_data['start_at']
        end_at = fixture_data['end_at']
        weekday = fixture_data['weekday']

        print("fixture_data=", fixture_data)
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
        fixtures_per_day = kwargs.get('fixtures_per_day', 2)
        # ref: https://docs.python.org/3/library/datetime.html#datetime.datetime.weekday
        # Saturday=5, Sunday=6, Monday=0
        fixtures_on_weekday = [
            5,
            6,
        ]
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
                for i in range(fixtures_per_day):
                    teams = random.sample(available_team_ids, 2)
                    print("random sample IDs ", teams)
                    fixture_data['home_team'] = teams[0]
                    fixture_data['away_team'] = teams[1]
                    fixture_data['start_at'] = fixture_start_at
                    fixture_data['end_at'] = fixture_end_at
                    fixture_data['weekday'] = fixture_start_at.weekday()
                    team, _ = FixtureApi.get_or_create(fixture_data)
                    fixtures.append(team)
        return fixtures

    @classmethod
    def list_all(cls):
        fixtures = Fixture.objects.all().order_by('-start_at')
        serializer = FixtureSerializer(fixtures, many=True)
        return serializer.data

    @classmethod
    def calendar_view(cls, month=None, year=None):
        now = timezone.make_aware(datetime.now())
        if not year:
            year = now.year
        if not month:
            month = now.month

        filter_q = Q(
            start_at__year=year,
            start_at__month=month,
        )
        fixtures = Fixture.objects.filter(filter_q).order_by('-start_at')
        serializer = FixtureSerializer(fixtures, many=True)
        return serializer.data
