import earthaccess
import xarray as xr
from pathlib import Path

# 1. LOG IN (uses the login you saved earlier)
earthaccess.login()

# 2. SEARCH for IMERG Late Run daily files, one week around the 2024-09-04 storm
# Box around Botolan: (west, south, east, north)
results = earthaccess.search_data(
    short_name="GPM_3IMERGDL",
    version="07",
    temporal=("2024-09-01", "2024-09-07"),
    bounding_box=(119.9, 15.2, 120.15, 15.4),
)
print("Files found:", len(results))

# 3. DOWNLOAD
Path("data/raw/imerg").mkdir(parents=True, exist_ok=True)
files = earthaccess.download(results, "data/raw/imerg")
print("Downloaded:", len(files), "files")

# 4. LOOK INSIDE the first file
ds = xr.open_dataset(files[0])
print(ds)