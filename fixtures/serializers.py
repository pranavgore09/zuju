from rest_framework import serializers

from fixtures.models import Fixture
from teams.serializers import TeamSerializer
from tournaments.serializers import TournamentSerializer


class FixtureSerializer(serializers.ModelSerializer):

    tournament = TournamentSerializer()
    home_team = TeamSerializer()
    away_team = TeamSerializer()
    weekday = serializers.SerializerMethodField()

    class Meta:
        model = Fixture
        fields = (
            'uuid',
            'tournament',
            'home_team',
            'away_team',
            'weekday',
            'state',
            'start_at',
            'end_at',
            'home_score',
            'away_score',
        )

    def get_weekday(self, obj):
        return Fixture.DAY_NAMES[obj.weekday][1]


class FixtureByCalendarSerializer(serializers.Serializer):
    date = serializers.DateField()
    fixture_count = serializers.IntegerField()
