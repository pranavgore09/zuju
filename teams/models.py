from django.db import models

from z_common.models import BaseDateTimeUUIDModel


# Teams can be created as a different app
class Team(BaseDateTimeUUIDModel):
    name = models.CharField(max_length=256, unique=True)

    def __str__(self) -> str:
        return f'Team:{self.name}'


# Many-To-Many table can be created for Team<>Tournament
