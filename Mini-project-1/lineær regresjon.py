import requests
import pandas as pd
from io import StringIO
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import linregress

# --- URLs ---
url_temp = "https://berkeley-earth-temperature.s3.us-west-1.amazonaws.com/Global/Land_and_Ocean_complete.txt"
url_co2  = "https://gml.noaa.gov/webdata/ccgg/trends/co2/co2_mm_gl.txt"

# --- Temperaturdata (bruk Month + Monthly anomaly) ---
r_temp = requests.get(url_temp).text
temp_raw = pd.read_csv(StringIO(r_temp),
                       comment='%', 
                       delim_whitespace=True, 
                       header=None,
                       skip_blank_lines=True)

# kolonne 0=Year, kolonne 1=Month, kolonne 2=Monthly anomaly
temp_df = temp_raw[[0,1,2]].copy()
temp_df.columns = ["Year","Month","TempAnom"]

# behold bare januar fra 1979 og utover
temp_jan = temp_df[(temp_df["Month"] == 1) & (temp_df["Year"] >= 1979)]
temp_jan = temp_jan[["Year","TempAnom"]].reset_index(drop=True)

# --- CO₂-data ---
r_co2 = requests.get(url_co2).text
co2_raw = pd.read_csv(StringIO(r_co2),
                      comment='#',
                      delim_whitespace=True,
                      header=None,
                      skip_blank_lines=True)

# col0=Year, col1=Month, col4=Interpolated CO₂
co2_df = co2_raw[[0,1,3]].copy()
co2_df.columns = ["Year","Month","CO2"]
co2_df = co2_df.replace(-99.99, pd.NA).dropna()

# behold kun januar fra 1979 og utover
co2_jan = co2_df[(co2_df["Month"] == 1) & (co2_df["Year"] >= 1979)]
co2_jan = co2_jan[["Year","CO2"]].reset_index(drop=True)

# --- slå sammen ---
merged = pd.merge(temp_jan, co2_jan, on="Year", how="inner")
merged = merged.sort_values("Year")

# --- Lineær regresjon (TempAnom -> CO₂) ---
slope, intercept, r_value, p_value, std_err = linregress(merged["TempAnom"], merged["CO2"])
r2 = r_value**2
print(f"R² = {r2:.3f}")
print(merged.head())

# --- Plot ---
plt.figure(figsize=(10,6))

# Scatter
sc = plt.scatter(merged["TempAnom"], merged["CO2"],
                 c=merged["Year"], cmap="plasma", s=30, edgecolor='k', linewidth=0.3,)

# Regresjonslinje
x_vals = np.linspace(merged["TempAnom"].min(), merged["TempAnom"].max(), 100)
y_vals = intercept + slope*x_vals
plt.plot(x_vals, y_vals, color="black", linestyle="--", linewidth=2, label=f"Regresjonslinje (R²={r2:.2f})")

# Layout
cbar = plt.colorbar(sc)
cbar.set_label("År")
plt.xlabel("Globalt temperaturavvik fra normalen (°C)")
plt.ylabel("CO₂ (ppm)")
plt.title("Temperaturavvik fra normalen og CO₂ (1979 - 2024, 1. måned hvert år)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
