from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class AccidentBase(BaseModel):
    id: str
    source: Optional[str] = None
    severity: Optional[int] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    start_lat: Optional[float] = None
    start_lng: Optional[float] = None
    end_lat: Optional[float] = None
    end_lng: Optional[float] = None
    distance_mi: Optional[float] = None
    description: Optional[str] = None
    street: Optional[str] = None
    city: Optional[str] = None
    county: Optional[str] = None
    state: Optional[str] = None
    zipcode: Optional[str] = None
    country: Optional[str] = None
    timezone: Optional[str] = None
    airport_code: Optional[str] = None
    weather_timestamp: Optional[datetime] = None
    temperature_f: Optional[float] = None
    wind_chill_f: Optional[float] = None
    humidity_pct: Optional[float] = None
    pressure_in: Optional[float] = None
    visibility_mi: Optional[float] = None
    wind_direction: Optional[str] = None
    wind_speed_mph: Optional[float] = None
    precipitation_in: Optional[float] = None
    weather_condition: Optional[str] = None
    amenity: Optional[bool] = None
    bump: Optional[bool] = None
    crossing: Optional[bool] = None
    give_way: Optional[bool] = None
    junction: Optional[bool] = None
    no_exit: Optional[bool] = None
    railway: Optional[bool] = None
    roundabout: Optional[bool] = None
    station: Optional[bool] = None
    stop: Optional[bool] = None
    traffic_calming: Optional[bool] = None
    traffic_signal: Optional[bool] = None
    turning_loop: Optional[bool] = None
    sunrise_sunset: Optional[str] = None
    civil_twilight: Optional[str] = None
    nautical_twilight: Optional[str] = None
    astronomical_twilight: Optional[str] = None


class AccidentRead(AccidentBase):
    model_config = ConfigDict(from_attributes=True)


class AccidentListResponse(BaseModel):
    items: list[AccidentRead]
    total: int


class StateCount(BaseModel):
    state: str
    total: int


class TopStatesResponse(BaseModel):
    items: list[StateCount]


class DayNightItem(BaseModel):
    period: str
    total: int


class DayNightResponse(BaseModel):
    items: list[DayNightItem]


class HourlyItem(BaseModel):
    hour: int
    total: int


class HourlyResponse(BaseModel):
    items: list[HourlyItem]


class WeekdayItem(BaseModel):
    iso_weekday: int
    weekday_name: str
    total: int


class WeekdayResponse(BaseModel):
    items: list[WeekdayItem]
