import random
from datetime import datetime, timedelta
from typing import List, Tuple

# from dateutil.relativedelta import relativedelta
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
        count = kwargs['count']
        months_in_past = 1
        days_in_past = 30 * months_in_past
        total_tournament_months = 2
        total_tournament_days = 30 * total_tournament_months

        tournaments = []
        allowed_titles = [
            'EPL',
            'SERIE A',
        ]
        now = timezone.make_aware(datetime.now())

        for i in range(count):
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
