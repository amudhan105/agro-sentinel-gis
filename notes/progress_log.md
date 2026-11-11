# Progress log (Amudhan S)

## 11 Nov 2026 - NASA competition sprint, NASA data day

### Done
- Built src/power_for_app.py: fetches NASA POWER daily data (T2M, RH2M,
  PRECTOTCORR, ALLSKY_SFC_SW_DWN) for a planning point near Botolan
  (15.29 N, 120.02 E), LST time standard
- Output: shared_data/power_botolan.json, 1096 days (2023-11-05 to 2026-11-04),
  with provenance (provider, units, dates, retrieval time, is_cached flag)
- Missing values: 1 in sunshine ([date from step 2]), none elsewhere
- Cached fallback: if NASA fails, the script reuses the saved file and
  marks it is_cached = true
- Monthly climate summary: shared_data/power_monthly_summary.csv
  (10 years, 2016-2025) for crop scoring [add only if step 1 ran]
- Placeholder field boundary: shared_data/pilot_plot.geojson
  (not a verified plot) [add only if step 3 done]

### Caveats
- POWER is a regional satellite/model-derived estimate, not a plot measurement
- Planning point and boundary are placeholders until the pilot plot and
  landowner permission are confirmed
- POWER vs IMERG disagreement on 4 Sept 2024 is still unexplained

### Waiting on team
- Confirm my role (Member 2?), pilot plot coordinates, data format needs

### Next
1. Check with the frontend developer that the JSON loads in AgriMind AI
2. Provide anything the analytics and research members need
3. Test SoilGrids with one request only if time allows

---

(earlier entries below)

## 10 Nov 2026 - Week 1










# Progress log (Amudhan S)

## 10 Nov 2026 - Week 1

### Setup done
- NASA Earthdata account, login tested from Python
- 64-bit Python 3.12 environment, GitHub repo (private)

### NASA POWER (point near 15.29 N, 120.02 E, 2016-2025)
- 3653 daily rows, no missing values
- Days with T2M above 35 C: 0
- Days with rain above 100 mm: 6 (largest 206.7 mm on 2024-09-04)
- Days with rain above 50 mm: 80
- Mean daily rain: wet season (Jun-Oct) 14.4 mm, dry season (Nov-May) 2.2 mm
- POWER is a coarse regional product, not a farm-scale measurement

### GPM IMERG Late daily V07, 0.1 degree (Sept 2024)
- 5x5 pixel box (about 50 km) around Botolan, 30 days, 750 rows
- Spread inside the box: median daily range 19.2 mm; largest 138.2 mm
  on 5 Sept (78 to 216 mm); 10 of 25 pixels above 100 mm that day
- Days where some, but not all, pixels exceeded 100 mm: 5
- Centre pixel vs POWER (30 days): bias -5.0 mm/day, MAE 15.8,
  RMSE 30.7, correlation 0.62; month total IMERG 737 mm, POWER 888 mm
- 4 Sept: POWER 207 mm, but no IMERG pixel in the box above 96.4 mm
- IMERG peak is one day after POWER peak; shifting POWER by +1 day
  gives r = 0.65 vs 0.62 (a hint only, 30 days)

### Caveats
- One month, one event, no ground rain-gauge data
- Neither product is ground truth; cannot say which is more accurate
- Cause of the 4 vs 5 Sept gap is not explained yet
  (not yet checked: POWER time standard and rainfall source)

### Next
1. Check POWER documentation (time standard, rainfall source)
2. Get elevation data (DEM) as a helper layer for downscaling
3. Ask team lead: definition of analog site research, and what
   ground data will be available for validation
4. Paco and Paudpod boundaries (QGIS or download)