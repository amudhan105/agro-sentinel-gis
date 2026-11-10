import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# ---------- Load ----------
imerg = pd.read_csv("data/imerg_botolan_box.csv", parse_dates=["date"])
power = pd.read_csv("data/raw/power_botolan_daily.csv",
                    index_col="date", parse_dates=True)

# ---------- Part 1: spread of the 25 pixels each day ----------
g = imerg.groupby("date")["precip_mm"]
daily = pd.DataFrame({
    "min": g.min(),
    "max": g.max(),
    "mean": g.mean(),
    "std": g.std(),
})
daily["range"] = daily["max"] - daily["min"]
daily["n_over_50"] = imerg[imerg.precip_mm > 50].groupby("date").size()
daily["n_over_100"] = imerg[imerg.precip_mm > 100].groupby("date").size()
daily = daily.fillna({"n_over_50": 0, "n_over_100": 0}).astype(float)

print("=== Spread of the 25 pixels, per day (mm) ===")
print(daily.round(1))

mixed = daily[(daily["n_over_100"] > 0) & (daily["n_over_100"] < 25)]
print("\nDays where SOME pixels (not all) exceeded 100 mm:", len(mixed))
print("Largest single-day range (max - min):", round(daily["range"].max(), 1),
      "mm on", daily["range"].idxmax().date())
print("Median daily range:", round(daily["range"].median(), 1), "mm")

# ---------- Part 2: IMERG centre pixel vs POWER ----------
centre = imerg[(imerg.lat.sub(15.25).abs() < 0.02) &
               (imerg.lon.sub(120.05).abs() < 0.02)]
centre = centre.set_index("date")["precip_mm"].rename("imerg_centre")

both = pd.concat([centre, power["PRECTOTCORR"].rename("power")],
                 axis=1, join="inner")

diff = both["imerg_centre"] - both["power"]
print("\n=== IMERG centre pixel vs POWER, Sept 2024 ===")
print("Days compared:", len(both))
print("Bias (IMERG minus POWER):", round(diff.mean(), 1), "mm/day")
print("MAE :", round(diff.abs().mean(), 1), "mm/day")
print("RMSE:", round(float(np.sqrt((diff ** 2).mean())), 1), "mm/day")
print("Correlation:", round(both["imerg_centre"].corr(both["power"]), 2))
print("Month total  IMERG:", round(both["imerg_centre"].sum(), 0),
      " POWER:", round(both["power"].sum(), 0), "mm")

# ---------- Part 3: day-shift test ----------
print("\n=== Day-shift test (correlation of IMERG with shifted POWER) ===")
for lag in (-1, 0, 1):
    shifted = power["PRECTOTCORR"].shift(lag).reindex(centre.index)
    print("POWER shifted by", lag, "day(s):",
          round(centre.corr(shifted), 2))

# ---------- Plot ----------
fig, ax = plt.subplots(figsize=(11, 4.5))
ax.fill_between(daily.index, daily["min"], daily["max"],
                color="lightblue", label="IMERG: min to max of 25 pixels")
ax.plot(daily.index, daily["mean"], color="tab:blue", label="IMERG mean of 25")
ax.plot(both.index, both["power"], color="tab:red", label="POWER")
ax.axhline(100, color="black", linestyle="--", linewidth=0.8,
           label="100 mm trigger")
ax.set_ylabel("Rain (mm/day)")
ax.set_title("Sept 2024: spread inside one IMERG box vs POWER")
ax.legend(fontsize=8)
plt.tight_layout()
Path("figures").mkdir(exist_ok=True)
plt.savefig("figures/blur_sept2024.png", dpi=150)
daily.round(2).to_csv("data/blur_daily_stats.csv")
print("\nSaved figures/blur_sept2024.png and data/blur_daily_stats.csv")
plt.show()