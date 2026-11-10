import os
import earthaccess
import pandas as pd
import xarray as xr
from pathlib import Path

# ---- Settings you can change ----
START, END = "2024-09-01", "2024-09-30"   # start with ONE month
LAT, LON = 15.29, 120.02
HALF = 0.25                                # box half-width in degrees (5 x 5 pixels)
OUT_CSV = Path("data/imerg_botolan_box.csv")
TMP = Path("data/raw/imerg_tmp")
# ---------------------------------

TMP.mkdir(parents=True, exist_ok=True)
OUT_CSV.parent.mkdir(parents=True, exist_ok=True)

done = set()
if OUT_CSV.exists():
    done = set(pd.read_csv(OUT_CSV)["date"].unique())
    print("Already done:", len(done), "days")

earthaccess.login()
results = earthaccess.search_data(
    short_name="GPM_3IMERGDL",
    version="07",
    temporal=(START, END),
)
print("Files found:", len(results))

for i, r in enumerate(results, 1):
    try:
        files = earthaccess.download([r], str(TMP))
        f = files[0]
        with xr.open_dataset(f) as ds:
            date = str(ds["time"].values[0])[:10]
            if date in done:
                print(date, "skipped")
            else:
                box = ds["precipitation"].isel(time=0).sel(
                    lat=slice(LAT - HALF, LAT + HALF),
                    lon=slice(LON - HALF, LON + HALF),
                )
                df = box.to_dataframe(name="precip_mm").reset_index()
                df = df[["lat", "lon", "precip_mm"]]
                df.insert(0, "date", date)
                df.to_csv(OUT_CSV, mode="a", header=not OUT_CSV.exists(), index=False)
                print(i, "/", len(results), date, "saved", len(df), "pixels")
        os.remove(f)        # delete the big file
    except Exception as e:
        print("Problem with item", i, ":", e)

print("Finished. Results in", OUT_CSV)