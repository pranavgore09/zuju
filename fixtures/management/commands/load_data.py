import random

from django.conf import settings
from django.core.management.base import BaseCommand

from fixtures.api import FixtureApi
from teams.api import TeamApi
from tournaments.api import TournamentApi


class Command(BaseCommand):
    '''
    Create Random Data for teams, tournaments, fixtures
    '''

    def handle(self, *args, **options):
        teams = TeamApi.bulk_create(count=settings.DEFAULT_TEAM_COUNT)
        tournaments = TournamentApi.bulk_create(
            count=settings.DEFAULT_TOURNAMENT_COUNT)
        fixtures = FixtureApi.bulk_create(
            tournament=random.sample(tournaments, 1))
