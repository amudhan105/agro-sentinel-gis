# NASA POWER data for AgriMind AI (Amudhan)

File: shared_data/power_botolan.json  (regenerate: python src/power_for_app.py)

## What it is
Daily NASA POWER Agroclimatology data for a planning point near Botolan
(15.29 N, 120.02 E), last 3 years. It is a satellite and model-derived
gridded estimate for a regional cell. It is NOT a measurement of one farm plot.

## Fields (per day)
- date: YYYY-MM-DD (local solar time, LST)
- T2M: air temperature at 2 m
- RH2M: relative humidity at 2 m
- PRECTOTCORR: corrected precipitation
- ALLSKY_SFC_SW_DWN: all-sky surface shortwave downward irradiance
Units are in metadata.parameters[...].unit.

## Provenance (metadata block)
provider, source_url, data_type, latitude, longitude, start, end,
time_standard, retrieved_at_utc, is_cached, missing_values.
If is_cached is true, show "cached copy retrieved at <time>" in the app.
Never present cached data as live.

## Assumptions I made (tell me if any are wrong)
1. JSON is fine; I can also give CSV.
2. One planning point near Botolan until a pilot plot is chosen.
3. Last 3 years of daily data is enough.
4. Missing values are null.

## Not provided yet
Soil data, vegetation index, plot boundary, crop calendar.