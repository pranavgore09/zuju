from django.core.management.base import BaseCommand

from fixtures.api import FixtureApi
from teams.api import TeamApi
from tournaments.api import TournamentApi


class Command(BaseCommand):
    '''
    Create Random Data for teams, tournaments, fixtures
    '''

    def handle(self, *args, **options):
        print(options)
        teams = TeamApi.bulk_create(count=5)
        tournaments = TournamentApi.bulk_create(count=1)
        fixtures_t1 = FixtureApi.bulk_create(tournament=tournaments[0])
        # fixtures_t2 = FixtureApi.bulk_create(tournament=tournaments[1])
