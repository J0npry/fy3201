import requests
import pandas as pd
from io import StringIO
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import linregress

# --- URLs ---
url_temp = "https://berkeley-earth-temperature.s3.us-west-1.amazonaws.com/Global/Land_and_Ocean_complete.txt"
url_co2  = "https://gml.noaa.gov/webdata/ccgg/trends/co2/co2_mm_gl.txt"


# temperaturdata
r_temp = requests.get(url_temp).text
temp_raw = pd.read_csv(StringIO(r_temp),
                       comment='%', 
                       delim_whitespace=True, 
                       header=None,
                       skip_blank_lines=True)

# kolonne 0=Year, kolonne 1=Month, kolonne 2=Monthly anomaly
temp_df = temp_raw[[0,1,2]].copy()
temp_df.columns = ["Year","Month","TempAnom"]


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


temp_all = temp_df[temp_df["Year"] >= 1979].reset_index(drop=True)
co2_all  = co2_df[co2_df["Year"] >= 1979].reset_index(drop=True)

# --- slå sammen på Year + Month ---
merged_all = pd.merge(temp_all, co2_all, on=["Year", "Month"], how="inner")
merged_all = merged_all.sort_values(["Year","Month"])

# --- Lineær regresjon (TempAnom -> CO₂) ---
slope, intercept, r_value, p_value, std_err = linregress(merged_all["TempAnom"], merged_all["CO2"])

# --- Plot ---
plt.figure(figsize=(10,6))

# Scatter
sc = plt.scatter(merged_all["TempAnom"], merged_all["CO2"],
                 c=merged_all["Year"], cmap="plasma", s=30, edgecolor='k', linewidth=0.3,)

# Regresjonslinje
x_vals = np.linspace(merged_all["TempAnom"].min(), merged_all["TempAnom"].max(), 100)
y_vals = intercept + slope*x_vals

# Regresjonslinje
plt.plot(x_vals, y_vals, color="black", linestyle="--", linewidth=2, label="Lineær regresjon")

# Scatter
sc = plt.scatter(merged_all["TempAnom"], merged_all["CO2"],
                 c=merged_all["Year"], cmap="plasma", s=30, edgecolor='k', linewidth=0.3)

# Fargebar
cbar = plt.colorbar(sc)
cbar.set_label("År")

# Tekst for Pearson r i øverste høyre hjørne
plt.text(
    0.95, 0.05,  # x=95% mot høyre, y=5% opp fra bunnen
    f"Korrelasjon = {r_value:.3f}",
    transform=plt.gca().transAxes,  # koordinater går fra 0-1 i aksen
    fontsize=12,
    color="black",
    ha="right",  # horisontal justering
    va="bottom"  # vertikal justering
)

# Labels og tittel
plt.xlabel("Globalt temperaturavvik fra normalen [°C]")
plt.ylabel("CO₂ i atmosfæren [ppm]")
plt.title("Temperaturavvik og CO₂ (1979 - 2024)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
