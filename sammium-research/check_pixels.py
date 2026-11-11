import glob
import xarray as xr

LAT, LON = 15.29, 120.02

for f in sorted(glob.glob("data/raw/imerg/*.nc*")):
    with xr.open_dataset(f) as ds:
        day = str(ds["time"].values[0])[:10]
        if day not in ("2024-09-04", "2024-09-05"):
            continue
        p = ds["precipitation"].isel(time=0)
        near = p.sel(lat=LAT, lon=LON, method="nearest")
        print("\n", day, "pixel centre:", float(near["lat"]), float(near["lon"]))
        box = p.sel(lat=slice(LAT - 0.15, LAT + 0.15),
                    lon=slice(LON - 0.15, LON + 0.15))
        print(box.transpose("lat", "lon").round(1).to_pandas())