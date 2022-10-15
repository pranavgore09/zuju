from datetime import datetime

from django.db.models import Count, F
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from fixtures.api import FixtureApi, FixtureSerializer
from fixtures.models import Fixture
from fixtures.pagination import FixtureCursorPagination
from fixtures.serializers import FixtureByCalendarSerializer, FixtureSerializer


class ListFixtures(ListAPIView):

    serializer_class = FixtureSerializer
    pagination_class = FixtureCursorPagination

    def get_queryset(self):
        tournament_uuid = self.kwargs.get('tournament_uuid', None)
        if not tournament_uuid:
            Fixture.objects.none()
        return Fixture.objects.filter(tournament__uuid=tournament_uuid)


class ListFixturesByCalendar(ListAPIView):

    serializer_class = FixtureByCalendarSerializer

    def get_queryset(self):
        tournament_uuid = self.kwargs.get('tournament_uuid', None)
        if not tournament_uuid:
            Fixture.objects.none()

        month = self.kwargs.get('month', 1)
        year = self.kwargs.get('year', datetime.now().year)
        return list(
            Fixture.objects.filter(
                tournament__uuid=tournament_uuid,
                start_at__year=year,
                start_at__month=month,
            ).values('start_at__date', ).annotate(
                fixture_count=Count('start_at__date', ),
                date=F('start_at__date', ),
            ).order_by('start_at__date'))
