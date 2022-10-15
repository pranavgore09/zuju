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


@api_view(http_method_names=[
    'GET',
])
def list_fixtures(request: Request):
    response = FixtureApi.list_all()
    return Response(data=response, status=status.HTTP_200_OK)


@api_view(http_method_names=[
    'GET',
])
def fixtures_by_calendar(request: Request, month=None):
    response = FixtureApi.calendar_view(month)
    return Response(data=response, status=status.HTTP_200_OK)


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
        return Fixture.objects.filter(start_at__month=month, ).values(
            'start_at__date', ).annotate(
                fixture_count=Count('start_at__date', ),
                date=F('start_at__date', ),
            ).order_by('start_at__date')
