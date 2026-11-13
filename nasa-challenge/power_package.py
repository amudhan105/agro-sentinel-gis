import json
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
import requests

# Placeholder point. Replace with the team's pilot plot coordinates.
LAT, LON = 15.29, 120.02
START, END = "20160101", "20251231"

URL = "https://power.larc.nasa.gov/api/temporal/daily/point"
params = {
    "parameters": "T2M,RH2M,PRECTOTCORR,ALLSKY_SFC_SW_DWN",
    "community": "AG",
    "longitude": LON,
    "latitude": LAT,
    "start": START,
    "end": END,
    "format": "JSON",
    "time-standard": "LST",
}

OUT = Path("package")      # not ignored by git, so teammates can use it
OUT.mkdir(exist_ok=True)

retrieved = datetime.now(timezone.utc).isoformat(timespec="seconds")
r = requests.get(URL, params=params, timeout=120)
r.raise_for_status()
payload = r.json()

# Cached copy of the raw response (label it "cached" if used in the demo)
(OUT / "power_raw_response.json").write_text(json.dumps(payload), encoding="utf-8")

# Clean table
df = pd.DataFrame(payload["properties"]["parameter"])
df.index = pd.to_datetime(df.index, format="%Y%m%d")
df.index.name = "date"
df = df.replace(-999, float("nan"))
df.to_csv(OUT / "power_botolan_daily.csv")

# Monthly averages (for crop calendar and water-need comparisons)
monthly = pd.DataFrame({
    "T2M_mean_C": df["T2M"].groupby(df.index.month).mean(),
    "RH2M_mean_pct": df["RH2M"].groupby(df.index.month).mean(),
    "solar_MJ_m2_day": df["ALLSKY_SFC_SW_DWN"].groupby(df.index.month).mean(),
})
month_totals = df["PRECTOTCORR"].groupby([df.index.year, df.index.month]).sum()
monthly["rain_mm_per_month_avg"] = month_totals.groupby(level=1).mean()
monthly.index.name = "month"
monthly.round(2).to_csv(OUT / "power_botolan_monthly.csv")

# Tests
checks = {
    "has_rows": len(df) > 3000,
    "no_missing": int(df.isna().sum().sum()) == 0,
    "T2M_plausible": bool(df["T2M"].between(10, 45).all()),
    "RH_plausible": bool(df["RH2M"].between(0, 100).all()),
    "rain_not_negative": bool((df["PRECTOTCORR"] >= 0).all()),
}

# Metadata (provenance)
pmeta = payload.get("parameters", {})
meta = {
    "provider": "NASA POWER (Prediction of Worldwide Energy Resources)",
    "endpoint": URL,
    "community": "AG",
    "data_type": "Satellite- and model-derived estimates, not a farm measurement",
    "latitude": LAT,
    "longitude": LON,
    "start": START,
    "end": END,
    "time_standard": "LST",
    "retrieved_utc": retrieved,
    "rows": len(df),
    "variables": {
        c: {"units": pmeta.get(c, {}).get("units"),
            "name": pmeta.get(c, {}).get("longname")}
        for c in df.columns
    },
    "missing_values": {c: int(v) for c, v in df.isna().sum().items()},
    "quality_checks": checks,
    "resolution_note": "Gridded regional product. Confirm exact grid size in POWER metadata before quoting.",
}
(OUT / "power_botolan_metadata.json").write_text(
    json.dumps(meta, indent=2), encoding="utf-8")

for k, v in checks.items():
    print(k, "OK" if v else "FAIL")
print("Saved files in", OUT.resolve())