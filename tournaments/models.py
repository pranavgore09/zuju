from django.db import models

from z_common.models import BaseDateTimeUUIDModel


class Tournament(BaseDateTimeUUIDModel):
    title = models.CharField(max_length=32, unique=True)
    start_at = models.DateTimeField(db_index=True)
    end_at = models.DateTimeField()

    # When we add User models we can use following fields for Audit purposes
    # created_by
    # modified_by

    def __str__(self) -> str:
        return f'Tournament:{self.title}'


# Many-To-Many table can be created for Team<>Tournament
