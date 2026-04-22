from django.contrib import admin

from .models import Accident


@admin.register(Accident)
class AccidentAdmin(admin.ModelAdmin):
    list_display = ("id", "severity", "city", "state", "start_time", "weather_condition")
    list_filter = ("severity", "state", "weather_condition")
    search_fields = ("id", "city", "county", "street", "description")
