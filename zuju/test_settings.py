from zuju.settings import *

ENVIRON = 'test'

FIXTURES_PER_DAY = 2
FIXTURES_ON_WEEKDAY = [
    5,  #Saturday
    6,  #Sunday
]
SUPPORTED_TOURNAMENT_TITLES = [
    'EPL',
]

# To be used while calculating start-end date for an tournament
DEFAULT_MONTHS_IN_PAST = 1
DEFAULT_TOURNAMENT_DURATION_IN_MONTHS = 1
DEFAULT_FIXTURE_PAGE_SIZE = 3
DEFAULT_TEAM_COUNT = 10
DEFAULT_TOURNAMENT_COUNT = 1
