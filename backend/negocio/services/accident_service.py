from negocio.schemas.accident_schemas import (
    AccidentListResponse,
    AccidentRead,
    DayNightItem,
    DayNightResponse,
    HourlyItem,
    HourlyResponse,
    StateCount,
    TopStatesResponse,
    WeekdayItem,
    WeekdayResponse,
)
from persistencia.repositories.accident_repository import (
    get_day_night_breakdown as get_day_night_breakdown_from_repo,
    get_hourly_distribution as get_hourly_distribution_from_repo,
    get_top_states as get_top_states_from_repo,
    get_weekday_distribution as get_weekday_distribution_from_repo,
    list_accidents as list_accidents_from_repo,
)

DEFAULT_LIMIT = 20
MAX_LIMIT = 100

WEEKDAY_NAMES = {
    1: "Monday",
    2: "Tuesday",
    3: "Wednesday",
    4: "Thursday",
    5: "Friday",
    6: "Saturday",
    7: "Sunday",
}


def get_accidents(
    *,
    limit: int = DEFAULT_LIMIT,
    offset: int = 0,
    state: str | None = None,
    severity: int | None = None,
) -> AccidentListResponse:
    bounded_limit = max(1, min(limit, MAX_LIMIT))
    bounded_offset = max(0, offset)

    rows, total = list_accidents_from_repo(
        limit=bounded_limit,
        offset=bounded_offset,
        state=state,
        severity=severity,
    )

    items = [AccidentRead.model_validate(accident) for accident in rows]
    return AccidentListResponse(items=items, total=total)


def get_top_states(*, limit: int = 10) -> TopStatesResponse:
    bounded_limit = max(1, min(limit, 50))
    rows = get_top_states_from_repo(limit=bounded_limit)
    items = [StateCount(state=row["state"], total=row["total"]) for row in rows]
    return TopStatesResponse(items=items)


def get_day_night_breakdown() -> DayNightResponse:
    rows = get_day_night_breakdown_from_repo()
    items = [DayNightItem(period=row["sunrise_sunset"], total=row["total"]) for row in rows]
    return DayNightResponse(items=items)


def get_hourly_distribution() -> HourlyResponse:
    rows = get_hourly_distribution_from_repo()
    items = [HourlyItem(hour=int(row["hour"]), total=row["total"]) for row in rows if row["hour"] is not None]
    return HourlyResponse(items=items)


def get_weekday_distribution() -> WeekdayResponse:
    rows = get_weekday_distribution_from_repo()
    items = [
        WeekdayItem(
            iso_weekday=int(row["iso_weekday"]),
            weekday_name=WEEKDAY_NAMES.get(int(row["iso_weekday"]), "Unknown"),
            total=row["total"],
        )
        for row in rows
        if row["iso_weekday"] is not None
    ]
    return WeekdayResponse(items=items)
