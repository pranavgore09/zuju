from zuju.settings import *

ENVIRON = 'local'

# Additional settings here

FIXTURES_PER_DAY = 2
FIXTURES_ON_WEEKDAY = [
    4,  #Friday
    5,  #Saturday
    6,  #Sunday
]

SUPPORTED_TOURNAMENT_TITLES = [
    'EPL',
    'SERIE A',
]

# To be used while calculating start-end date for an tournament
DEFAULT_MONTHS_IN_PAST = 3
DEFAULT_TOURNAMENT_DURATION_IN_MONTHS = 10

DEFAULT_FIXTURE_PAGE_SIZE = 3

DEFAULT_TEAM_COUNT = 10

DEFAULT_TOURNAMENT_COUNT = 1
