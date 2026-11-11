import json
import pandas as pd
from pathlib import Path

SRC = "data/raw/power_botolan_daily.csv"
df = pd.read_csv(SRC, index_col="date", parse_dates=True)

monthly = pd.DataFrame({
    "rain_mm": df["PRECTOTCORR"].resample("MS").sum(),
    "T2M": df["T2M"].resample("MS").mean(),
    "RH2M": df["RH2M"].resample("MS").mean(),
    "SW": df["ALLSKY_SFC_SW_DWN"].resample("MS").mean(),
})
monthly["month"] = monthly.index.month

summary = monthly.groupby("month").agg(
    rain_mean_mm=("rain_mm", "mean"),
    rain_std_mm=("rain_mm", "std"),
    rain_min_mm=("rain_mm", "min"),
    rain_max_mm=("rain_mm", "max"),
    T2M_mean_C=("T2M", "mean"),
    RH2M_mean_pct=("RH2M", "mean"),
    sunshine_mean_MJ_m2_day=("SW", "mean"),
).round(1)

# Planning assumption from the team document: wet season Jun-Oct
summary["season_assumed"] = [
    "wet" if m in (6, 7, 8, 9, 10) else "dry" for m in summary.index
]

print(summary)
print("\nYears used:", df.index.year.min(), "to", df.index.year.max())

Path("shared_data").mkdir(exist_ok=True)
summary.to_csv("shared_data/power_monthly_summary.csv")

meta = {
    "provider": "NASA POWER (Agroclimatology community)",
    "years_used": [int(df.index.year.min()), int(df.index.year.max())],
    "point": {"latitude": 15.29, "longitude": 120.02},
    "note": ("Monthly climatology from daily regional estimates, "
             "not farm-plot measurements. Time standard for this file "
             "was the API default, not set explicitly."),
    "rain_mean_mm": "average of the monthly totals across years",
}
Path("shared_data/power_monthly_summary_meta.json").write_text(
    json.dumps(meta, indent=1), encoding="utf-8")
print("Saved shared_data/power_monthly_summary.csv and _meta.json")