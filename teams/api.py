from typing import List, Tuple

from faker import Faker
from faker.providers import company

from teams.models import Team


class TeamApi:

    @classmethod
    def get_or_create(cls, *args, **kwargs) -> Tuple[Team, bool]:
        name = kwargs['name']
        return Team.objects.get_or_create(name=name)

    @classmethod
    def bulk_create(cls, *args, **kwargs) -> List[Team]:
        count = kwargs['count']
        teams = []
        fake = Faker()
        fake.add_provider(company)
        for i in range(count):
            name = fake.company()
            team, _ = TeamApi.get_or_create(name=name)
            teams.append(team)
        return teams
