import imp

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from fixtures.api import FixtureApi


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
