# agro-sentinel-gis

GIS and remote sensing work for the Sammium Agro-Sentinel project
(pilot area: Botolan, Zambales, Philippines).
Owner: Amudhan S (GIS and Remote Sensing).

## Goal
Turn coarse satellite data into useful information for small farm plots,
and report how uncertain it is.

## Setup (Windows, 64-bit Python 3.12)
    py -3.12 -m venv .venv
    .venv\Scripts\activate
    pip install -r requirements.txt

NASA Earthdata account needed for IMERG:
    python -c "import earthaccess; earthaccess.login(persist=True)"
Never put passwords in code or commit them.

## Scripts (src/)
- fetch_power.py: NASA POWER daily weather, 2016-2025, one point near Botolan
- check_power.py: counts of threshold days, monthly rain, wet vs dry season
- plot_seasons.py: rain graph with wet season shaded
- fetch_imerg_test.py: one-week GPM IMERG Late test download
- compare_imerg_power.py: IMERG centre pixel vs POWER, 1-7 Sept 2024
- check_pixels.py: neighbouring IMERG pixels on 4 and 5 Sept 2024
- extract_imerg.py: downloads one IMERG day at a time, keeps a 5x5 pixel box
  around Botolan, deletes the big file (safe for low-RAM laptops)
- analyze_blur.py: spread of pixels inside the box, IMERG vs POWER stats
- power_for_app.py: app-ready NASA POWER JSON with provenance and cached fallback
- monthly_summary.py: monthly climate summary for crop scoring

## Data
The data/ folder is not in git. Recreate it by running the scripts.

## Status
See notes/progress_log.md