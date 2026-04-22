from django.db import models


class Accident(models.Model):
    id = models.CharField(primary_key=True, max_length=20)
    source = models.CharField(max_length=32, null=True, blank=True)
    severity = models.SmallIntegerField(null=True, blank=True)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    start_lat = models.FloatField(null=True, blank=True)
    start_lng = models.FloatField(null=True, blank=True)
    end_lat = models.FloatField(null=True, blank=True)
    end_lng = models.FloatField(null=True, blank=True)
    distance_mi = models.FloatField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    street = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    county = models.CharField(max_length=255, null=True, blank=True)
    state = models.CharField(max_length=2, null=True, blank=True)
    zipcode = models.CharField(max_length=20, null=True, blank=True)
    country = models.CharField(max_length=2, null=True, blank=True)
    timezone = models.CharField(max_length=64, null=True, blank=True)
    airport_code = models.CharField(max_length=10, null=True, blank=True)
    weather_timestamp = models.DateTimeField(null=True, blank=True)
    temperature_f = models.FloatField(null=True, blank=True)
    wind_chill_f = models.FloatField(null=True, blank=True)
    humidity_pct = models.FloatField(null=True, blank=True)
    pressure_in = models.FloatField(null=True, blank=True)
    visibility_mi = models.FloatField(null=True, blank=True)
    wind_direction = models.CharField(max_length=32, null=True, blank=True)
    wind_speed_mph = models.FloatField(null=True, blank=True)
    precipitation_in = models.FloatField(null=True, blank=True)
    weather_condition = models.CharField(max_length=255, null=True, blank=True)
    amenity = models.BooleanField(null=True, blank=True)
    bump = models.BooleanField(null=True, blank=True)
    crossing = models.BooleanField(null=True, blank=True)
    give_way = models.BooleanField(null=True, blank=True)
    junction = models.BooleanField(null=True, blank=True)
    no_exit = models.BooleanField(null=True, blank=True)
    railway = models.BooleanField(null=True, blank=True)
    roundabout = models.BooleanField(null=True, blank=True)
    station = models.BooleanField(null=True, blank=True)
    stop = models.BooleanField(null=True, blank=True)
    traffic_calming = models.BooleanField(null=True, blank=True)
    traffic_signal = models.BooleanField(null=True, blank=True)
    turning_loop = models.BooleanField(null=True, blank=True)
    sunrise_sunset = models.CharField(max_length=8, null=True, blank=True)
    civil_twilight = models.CharField(max_length=8, null=True, blank=True)
    nautical_twilight = models.CharField(max_length=8, null=True, blank=True)
    astronomical_twilight = models.CharField(max_length=8, null=True, blank=True)

    class Meta:
        db_table = "us_accidents"
        managed = False
        ordering = ["-start_time"]
        indexes = [
            models.Index(fields=["start_time"], name="idx_us_acc_start_time"),
            models.Index(fields=["state"], name="idx_us_acc_state"),
            models.Index(fields=["city"], name="idx_us_acc_city"),
            models.Index(fields=["severity"], name="idx_us_acc_severity"),
            models.Index(fields=["start_lat", "start_lng"], name="idx_us_acc_lat_lng"),
        ]

    def __str__(self):
        return f"{self.id} | {self.city}, {self.state}"
