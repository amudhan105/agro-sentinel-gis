import requests
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Approximate centre of Botolan, Zambales (we will refine this later
# with the real Paco and Paudpod boundaries)
LAT, LON = 15.29, 120.02
START, END = "20160101", "20251231"   # about 10 years

URL = "https://power.larc.nasa.gov/api/temporal/daily/point"
PARAMS = {
    "parameters": "T2M,RH2M,PRECTOTCORR,ALLSKY_SFC_SW_DWN",
    "community": "AG",
    "longitude": LON,
    "latitude": LAT,
    "start": START,
    "end": END,
    "format": "JSON",
}

# 1. FETCH
print("Downloading from NASA POWER...")
response = requests.get(URL, params=PARAMS, timeout=120)
response.raise_for_status()
payload = response.json()
df = pd.DataFrame(payload["properties"]["parameter"])

# 2. CLEAN
df.index = pd.to_datetime(df.index, format="%Y%m%d")
df.index.name = "date"
df = df.replace(-999, float("nan"))   # POWER uses -999 for "no data"

# 3. CHECK
print("\nRows:", len(df))
print("Date range:", df.index.min().date(), "to", df.index.max().date())
print("\nMissing values per column:")
print(df.isna().sum())
print("\nSummary:")
print(df.describe().round(2))

# Save the cleaned data (the data folder is ignored by git)
Path("data/raw").mkdir(parents=True, exist_ok=True)
df.to_csv("data/raw/power_botolan_daily.csv")

# 4. PLOT
fig, axes = plt.subplots(2, 1, figsize=(11, 7), sharex=True)
df["T2M"].plot(ax=axes[0], color="tab:red", linewidth=0.7)
axes[0].set_ylabel("Air temperature (deg C)")
axes[0].set_title("NASA POWER daily data near Botolan, Zambales")
df["PRECTOTCORR"].plot(ax=axes[1], color="tab:blue", linewidth=0.7)
axes[1].set_ylabel("Rainfall (mm/day)")
plt.tight_layout()
Path("figures").mkdir(exist_ok=True)
plt.savefig("figures/power_botolan.png", dpi=150)
print("\nSaved figures/power_botolan.png")
plt.show()