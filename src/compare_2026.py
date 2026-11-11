import json
import pandas as pd

d = json.load(open("shared_data/power_botolan.json", encoding="utf-8"))
df = pd.DataFrame(d["records"])
df["date"] = pd.to_datetime(df["date"])
df = df.set_index("date")

rain26 = df.loc["2026-01-01":"2026-10-31", "PRECTOTCORR"].resample("MS").sum()
clim = pd.read_csv("shared_data/power_monthly_summary.csv", index_col="month")

out = pd.DataFrame({"rain_2026_mm": rain26.values}, index=rain26.index.month)
out["clim_mean_mm"] = clim.loc[out.index, "rain_mean_mm"]
out["clim_std_mm"] = clim.loc[out.index, "rain_std_mm"]
out["diff_mm"] = out["rain_2026_mm"] - out["clim_mean_mm"]
out["diff_in_std"] = out["diff_mm"] / out["clim_std_mm"]
print(out.round(1))