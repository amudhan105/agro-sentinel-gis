import pandas as pd

df = pd.read_csv("data/raw/power_botolan_daily.csv", index_col="date", parse_dates=True)

print("Days with T2M > 35 C:", (df["T2M"] > 35).sum())
print("Days with rain > 100 mm:", (df["PRECTOTCORR"] > 100).sum())
print("Days with rain > 50 mm:", (df["PRECTOTCORR"] > 50).sum())

# Which dates had the extreme rain?
print("\nHeaviest rain days:")
print(df["PRECTOTCORR"].nlargest(5).round(1))

# Average rain per month, to see wet and dry seasons
monthly = df["PRECTOTCORR"].groupby(df.index.month).mean().round(1)
print("\nAverage daily rain by month (1=Jan ... 12=Dec):")
print(monthly)

# Wet season (Jun-Oct) versus dry season (Nov-May)
wet = df[df.index.month.isin([6, 7, 8, 9, 10])]["PRECTOTCORR"].mean()
dry = df[~df.index.month.isin([6, 7, 8, 9, 10])]["PRECTOTCORR"].mean()
print(f"\nMean daily rain, wet season: {wet:.1f} mm")
print(f"Mean daily rain, dry season: {dry:.1f} mm")