import random
from datetime import datetime, timedelta
from typing import List, Tuple

from django.conf import settings
from django.utils import timezone

from tournaments.models import Tournament


class TournamentApi:

    @classmethod
    def get_or_create(cls, *args, **kwargs) -> Tuple[Tournament, bool]:
        title = kwargs.get('title')
        start_at = kwargs.get('start_at')
        end_at = kwargs.get('end_at')
        return Tournament.objects.get_or_create(
            title=title,
            defaults={
                'start_at': start_at,
                'end_at': end_at,
            },
        )

    @classmethod
    def bulk_create(cls, *args, **kwargs) -> List[Tournament]:
        count = kwargs.get('count', settings.DEFAULT_TOURNAMENT_COUNT)
        months_in_past = settings.DEFAULT_MONTHS_IN_PAST
        days_in_past = 30 * months_in_past
        total_tournament_months = settings.DEFAULT_TOURNAMENT_DURATION_IN_MONTHS
        total_tournament_days = 30 * total_tournament_months

        tournaments = []
        allowed_titles = settings.SUPPORTED_TOURNAMENT_TITLES
        now = timezone.make_aware(datetime.now())

        for _ in range(count):
            title = random.sample(allowed_titles, 1)
            start_at = now - timedelta(days=days_in_past)
            end_at = start_at + timedelta(days=total_tournament_days)
            tournament, _ = TournamentApi.get_or_create(
                title=title[0],
                start_at=start_at,
                end_at=end_at,
            )
            tournaments.append(tournament)
        return tournaments
