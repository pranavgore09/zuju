'''
Usage:
./manage.py test fixtures.tests --settings=zuju.test_settings --failfast
'''

from datetime import datetime

import time_machine
from django.conf import settings
from django.test import TestCase
from django.urls import reverse
from django.utils.timezone import get_current_timezone
from rest_framework import status
from rest_framework.test import APITestCase

from fixtures.api import FixtureApi
from fixtures.models import Fixture
from teams.api import TeamApi
from teams.models import Team
from tournaments.api import TournamentApi
from tournaments.models import Tournament


class TestFactoryMethods(TestCase):
    '''
    
    Usage:
    ./manage.py test fixtures.tests.TestFactoryMethods --settings=zuju.test_settings --failfast
    '''

    @time_machine.travel(
        datetime(2022, 10, 15, 10, 10, 0, 0, tzinfo=get_current_timezone()))
    def test_factory_creation(self):
        '''
        Usage:
        ./manage.py test fixtures.tests.TestFactoryMethods.test_factory_creation --settings=zuju.test_settings --failfast
        '''
        # Start with clean slate
        Team.objects.all().delete()
        Tournament.objects.all().delete()
        Fixture.objects.all().delete()

        # Test each factory method

        # Test teams factory
        expected_teams_count = settings.DEFAULT_TEAM_COUNT
        teams = TeamApi.bulk_create(count=settings.DEFAULT_TEAM_COUNT)
        self.assertEqual(len(teams), expected_teams_count)
        self.assertEqual(Team.objects.all().count(), expected_teams_count)

        # Test tournament factory
        expected_tournament_count = settings.DEFAULT_TOURNAMENT_COUNT
        tournaments = TournamentApi.bulk_create()
        self.assertEqual(len(tournaments), expected_tournament_count)
        self.assertEqual(Tournament.objects.all().count(),
                         expected_tournament_count)

        # Test Fixture Factory
        expected_fixture_count = 16
        fixtures = FixtureApi.bulk_create(tournament=tournaments[0])

        # Because of the variable time of test running it is producing variable result
        #   based on number of saturdays and sundays in the given period
        self.assertTrue(
            (expected_fixture_count -
             3) <= Fixture.objects.all().count() <= expected_fixture_count + 3)


class TestFixturesAPI(APITestCase):
    '''
    
    Usage:
    ./manage.py test fixtures.tests.TestFixturesAPI --settings=zuju.test_settings --failfast
    '''

    def setUp(self):
        # Start with clean slate
        Team.objects.all().delete()
        Tournament.objects.all().delete()
        Fixture.objects.all().delete()

        TeamApi.bulk_create(count=settings.DEFAULT_TEAM_COUNT)
        TournamentApi.bulk_create()

    def test_empty_response(self):
        '''    
        Usage:
        ./manage.py test fixtures.tests.TestFixturesAPI.test_empty_response --settings=zuju.test_settings --failfast
        '''
        tournament = Tournament.objects.first()
        url = reverse('fixture_list',
                      kwargs={'tournament_uuid': str(tournament.uuid)})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual([], response.data.get('results'))

    def test_fixtures_pagination(self):
        '''    
        Usage:
        ./manage.py test fixtures.tests.TestFixturesAPI.test_fixtures_pagination --settings=zuju.test_settings --failfast
        '''
        tournament = Tournament.objects.first()
        fixtures = FixtureApi.bulk_create(tournament=tournament)
        url = reverse('fixture_list',
                      kwargs={'tournament_uuid': str(tournament.uuid)})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(settings.DEFAULT_FIXTURE_PAGE_SIZE,
                         len(response.data.get('results')))

        next_url = response.data['next']
        response = self.client.get(next_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data.get('results')) > 0)


class TestFixturesCalendarAPI(APITestCase):
    '''    
    Usage:
    ./manage.py test fixtures.tests.TestFixturesCalendarAPI --settings=zuju.test_settings --failfast
    '''

    FIXED_DATE = datetime(2022,
                          10,
                          15,
                          10,
                          10,
                          0,
                          0,
                          tzinfo=get_current_timezone())

    @time_machine.travel(FIXED_DATE)
    def setUp(self):
        # Start with clean slate
        Team.objects.all().delete()
        Tournament.objects.all().delete()
        Fixture.objects.all().delete()

        self.teams = TeamApi.bulk_create(count=settings.DEFAULT_TEAM_COUNT)
        self.tournament = TournamentApi.bulk_create()[0]

        self.fixture1 = {
            'tournament': self.tournament.id,
            'home_team': self.teams[0].id,
            'away_team': self.teams[1].id,
            'start_at': self.FIXED_DATE,
            'end_at': self.FIXED_DATE,
            'weekday': 6
        }
        FixtureApi.get_or_create(self.fixture1)
        self.fixture1 = {
            'tournament': self.tournament.id,
            'home_team': self.teams[3].id,
            'away_team': self.teams[4].id,
            'start_at': self.FIXED_DATE,
            'end_at': self.FIXED_DATE,
            'weekday': 6
        }
        FixtureApi.get_or_create(self.fixture1)

    def test_fixtures_calendar(self):
        '''    
        Usage:
        ./manage.py test fixtures.tests.TestFixturesCalendarAPI.test_fixtures_calendar --settings=zuju.test_settings --failfast
        '''
        url = reverse('fixture_by_cal',
                      kwargs={
                          'tournament_uuid': str(self.tournament.uuid),
                          'month': 10,
                      })
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.data)
        self.assertEqual(1, len(response.data))
        self.assertEqual('2022-10-15', response.data[0]['date'])
        self.assertEqual(2, response.data[0]['fixture_count'])
