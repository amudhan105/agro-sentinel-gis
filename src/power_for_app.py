import json
import requests
import pandas as pd
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

LAT, LON = 15.29, 120.02          # approximate Botolan, planning point
END = date.today() - timedelta(days=7)      # POWER lags a few days
START = END - timedelta(days=3 * 365)
OUT = Path("shared_data/power_botolan.json")

URL = "https://power.larc.nasa.gov/api/temporal/daily/point"
PARAMS = {
    "parameters": "T2M,RH2M,PRECTOTCORR,ALLSKY_SFC_SW_DWN",
    "community": "AG",
    "longitude": LON,
    "latitude": LAT,
    "start": START.strftime("%Y%m%d"),
    "end": END.strftime("%Y%m%d"),
    "format": "JSON",
    "time-standard": "LST",
}

OUT.parent.mkdir(exist_ok=True)

try:
    r = requests.get(URL, params=PARAMS, timeout=120)
    r.raise_for_status()
    payload = r.json()
    df = pd.DataFrame(payload["properties"]["parameter"])
    df.index = pd.to_datetime(df.index, format="%Y%m%d")
    df = df.where(df != -999)               # -999 means no data

    units = {k: v.get("units") for k, v in payload.get("parameters", {}).items()}
    records = []
    for d, row in df.iterrows():
        rec = {"date": d.strftime("%Y-%m-%d")}
        for col, val in row.items():
            rec[col] = None if pd.isna(val) else round(float(val), 3)
        records.append(rec)

    out = {
        "metadata": {
            "provider": "NASA POWER (Agroclimatology community)",
            "source_url": URL,
            "data_type": "satellite and model-derived gridded estimate (not a farm measurement)",
            "latitude": LAT,
            "longitude": LON,
            "start": START.isoformat(),
            "end": END.isoformat(),
            "time_standard": "LST",
            "parameters": {
                "T2M": {"name": "Air temperature at 2 m", "unit": units.get("T2M")},
                "RH2M": {"name": "Relative humidity at 2 m", "unit": units.get("RH2M")},
                "PRECTOTCORR": {"name": "Corrected precipitation", "unit": units.get("PRECTOTCORR")},
                "ALLSKY_SFC_SW_DWN": {"name": "All-sky surface shortwave downward irradiance", "unit": units.get("ALLSKY_SFC_SW_DWN")},
            },
            "spatial_resolution_note": "Regional grid cell; check current POWER metadata for exact size",
            "retrieved_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "is_cached": False,
            "missing_values": {c: int(df[c].isna().sum()) for c in df.columns},
        },
        "records": records,
    }
    OUT.write_text(json.dumps(out, indent=1), encoding="utf-8")
    print("LIVE fetch OK:", len(records), "days,", START, "to", END)

except Exception as e:
    print("Live fetch failed:", e)
    if OUT.exists():
        out = json.loads(OUT.read_text(encoding="utf-8"))
        out["metadata"]["is_cached"] = True
        print("Using CACHED copy retrieved at", out["metadata"]["retrieved_at_utc"])
    else:
        raise

m = out["metadata"]
print("Provider:", m["provider"])
print("Units:", {k: v["unit"] for k, v in m["parameters"].items()})
print("Missing values:", m["missing_values"])
print("is_cached:", m["is_cached"])