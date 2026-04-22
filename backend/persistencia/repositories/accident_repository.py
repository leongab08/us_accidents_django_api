from django.db.models import Count
from django.db.models.functions import ExtractHour, ExtractIsoWeekDay

from persistencia.models import Accident


def _build_queryset(*, state: str | None = None, severity: int | None = None):
    queryset = Accident.objects.all()
    if state:
        queryset = queryset.filter(state__iexact=state)
    if severity is not None:
        queryset = queryset.filter(severity=severity)
    return queryset


def list_accidents(
    *,
    limit: int,
    offset: int,
    state: str | None = None,
    severity: int | None = None,
):
    queryset = _build_queryset(state=state, severity=severity)
    total = queryset.count()
    items = list(queryset[offset : offset + limit])
    return items, total


def get_top_states(*, limit: int):
    queryset = (
        Accident.objects.exclude(state__isnull=True)
        .exclude(state="")
        .values("state")
        .annotate(total=Count("id"))
        .order_by("-total", "state")[:limit]
    )
    return list(queryset)


def get_day_night_breakdown():
    queryset = (
        Accident.objects.filter(sunrise_sunset__in=["Day", "Night"])
        .values("sunrise_sunset")
        .annotate(total=Count("id"))
        .order_by("sunrise_sunset")
    )
    return list(queryset)


def get_hourly_distribution():
    queryset = (
        Accident.objects.exclude(start_time__isnull=True)
        .annotate(hour=ExtractHour("start_time"))
        .values("hour")
        .annotate(total=Count("id"))
        .order_by("hour")
    )
    return list(queryset)


def get_weekday_distribution():
    queryset = (
        Accident.objects.exclude(start_time__isnull=True)
        .annotate(iso_weekday=ExtractIsoWeekDay("start_time"))
        .values("iso_weekday")
        .annotate(total=Count("id"))
        .order_by("iso_weekday")
    )
    return list(queryset)
