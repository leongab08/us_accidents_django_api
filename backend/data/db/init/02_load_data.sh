#!/bin/bash
set -euo pipefail

CSV_PATH="/data/US_Accidents_March23.csv"

if [ ! -f "$CSV_PATH" ]; then
  echo "CSV file not found at $CSV_PATH. Skipping data load (schema-only mode)."
  exit 0
fi

echo "Checking if us_accidents already has data..."
row_count="$(psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" -tAc "SELECT COUNT(*) FROM us_accidents;")"
row_count="${row_count//[[:space:]]/}"

if [ "$row_count" != "0" ]; then
  echo "Table already has $row_count rows. Skipping load."
  exit 0
fi

echo "Loading CSV data into us_accidents..."
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<'SQL'
COPY us_accidents (
  id,
  source,
  severity,
  start_time,
  end_time,
  start_lat,
  start_lng,
  end_lat,
  end_lng,
  distance_mi,
  description,
  street,
  city,
  county,
  state,
  zipcode,
  country,
  timezone,
  airport_code,
  weather_timestamp,
  temperature_f,
  wind_chill_f,
  humidity_pct,
  pressure_in,
  visibility_mi,
  wind_direction,
  wind_speed_mph,
  precipitation_in,
  weather_condition,
  amenity,
  bump,
  crossing,
  give_way,
  junction,
  no_exit,
  railway,
  roundabout,
  station,
  stop,
  traffic_calming,
  traffic_signal,
  turning_loop,
  sunrise_sunset,
  civil_twilight,
  nautical_twilight,
  astronomical_twilight
) FROM '/data/US_Accidents_March23.csv'
WITH (FORMAT csv, HEADER true, NULL '', QUOTE '"', ESCAPE '"');
SQL

echo "CSV load completed."
