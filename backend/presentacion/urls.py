from django.urls import path

from presentacion.views import (
    ask_accidents,
    day_night_breakdown,
    health,
    hourly_distribution,
    list_accidents,
    llm_tools,
    top_states,
    weekday_distribution,
)

urlpatterns = [
    path("health/", health, name="health"),
    path("accidents/", list_accidents, name="accidents-list"),
    path("analytics/top-states/", top_states, name="analytics-top-states"),
    path("analytics/day-night/", day_night_breakdown, name="analytics-day-night"),
    path("analytics/hourly/", hourly_distribution, name="analytics-hourly"),
    path("analytics/weekday/", weekday_distribution, name="analytics-weekday"),
    path("llm/tools/", llm_tools, name="llm-tools"),
    path("llm/ask/", ask_accidents, name="llm-ask"),
]
