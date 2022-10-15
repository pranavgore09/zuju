from django.contrib import admin
from django.db.models.query_utils import Q
from django.utils.translation import gettext as _


# Register your models here.
class BaseUUIDAdmin(admin.ModelAdmin):

    readonly_fields = (
        'uuid',
        'created_at',
        'modified_at',
    )


class InputFilter(admin.SimpleListFilter):
    # Generic Input Filter
    # ref: https://hakibenita.com/how-to-add-a-text-filter-to-django-admin

    template = 'admin/input_filter.html'

    def lookups(self, request, model_admin):
        # Dummy, required to show the filter.
        return ((), )

    def choices(self, changelist):
        # Grab only the "all" option.
        all_choice = next(super().choices(changelist))
        all_choice['query_parts'] = ((
            k, v) for k, v in changelist.get_filters_params().items()
                                     if k != self.parameter_name)
        yield all_choice


class TournamentSearch(InputFilter):
    # works with a "tournament" column in the model
    # ref: https://hakibenita.com/how-to-add-a-text-filter-to-django-admin

    # what it'll be called in the url
    parameter_name = 'tournament'

    # what will show up on UI
    title = _('Tournament')

    def queryset(self, request, queryset):
        if self.value() is not None:
            name = self.value()

            return queryset.filter(tournament__title__icontains=name)


class TeamSearch(InputFilter):

    # what it'll be called in the url
    parameter_name = 'team'

    # what will show up on UI
    title = _('Team')

    def queryset(self, request, queryset):
        if self.value() is not None:
            name = self.value()

            return queryset.filter(
                Q(home_team__name__icontains=name)
                | Q(away_team__name__icontains=name))
