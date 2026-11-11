# NASA data for AgriMind AI (owner: Amudhan)

## What is here
- datasets/power_botolan.json: 3 years of daily NASA POWER data for a
  planning point near Botolan (15.29 N, 120.02 E), with provenance
- datasets/power_monthly_summary.csv: 2016-2025 monthly climate (mean,
  spread, min, max) for crop-calendar scoring
  (power_monthly_summary_meta.json explains it)
- datasets/pilot_plot.geojson: PLACEHOLDER boundary, not a verified plot
- src/: scripts that rebuild the files above

## What the data is (please label this in the app)
Satellite and model-derived regional estimate. NOT a farm measurement.

## JSON structure
{ "metadata": { provider, units, dates, retrieved_at_utc, is_cached, ... },
  "records": [ {date, T2M, RH2M, PRECTOTCORR, ALLSKY_SFC_SW_DWN}, ... ] }
- null = missing value (do not treat as zero)
- If metadata.is_cached is true, show "cached copy" in the app,
  never "live"

## Load it (JavaScript)
  const r = await fetch("power_botolan.json");
  const d = await r.json();
  // d.metadata.provider, d.metadata.retrieved_at_utc, d.records[...]

## Rebuild it
  python nasa-challenge/src/power_for_app.py
  python nasa-challenge/src/monthly_summary.py

## Limits
- Regional grid cell, not a plot
- 10-year climatology is short
- August 2026 was extremely wet (about 1362 mm by POWER); the exact
  amount is unverified and needs gauge data