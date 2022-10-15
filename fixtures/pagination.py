from django.conf import settings
from rest_framework.pagination import CursorPagination


class FixtureCursorPagination(CursorPagination):
    page_size = settings.DEFAULT_FIXTURE_PAGE_SIZE
    ordering = 'created_at'
