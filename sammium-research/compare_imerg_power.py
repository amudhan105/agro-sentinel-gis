import glob
import pandas as pd
import xarray as xr

LAT, LON = 15.29, 120.02   # same point we used for POWER

rows = []
for f in sorted(glob.glob("data/raw/imerg/*.nc*")):
    with xr.open_dataset(f) as ds:
        # pick the one pixel nearest to Botolan
        pt = ds["precipitation"].sel(lat=LAT, lon=LON, method="nearest")
        rows.append({
            "date": pd.Timestamp(ds["time"].values[0]).normalize(),
            "imerg_mm": float(pt.values[0]),
            "pixel_lat": float(pt["lat"]),
            "pixel_lon": float(pt["lon"]),
        })

imerg = pd.DataFrame(rows).set_index("date")

power = pd.read_csv("data/raw/power_botolan_daily.csv",
                    index_col="date", parse_dates=True)

out = imerg.join(power["PRECTOTCORR"].rename("power_mm"))
out["difference_mm"] = out["imerg_mm"] - out["power_mm"]

print(out.round(1))
out.to_csv("data/imerg_vs_power_test.csv")