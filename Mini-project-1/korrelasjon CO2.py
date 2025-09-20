import requests
import numpy as np
import matplotlib.pyplot as plt

# --- Hent CO2-data ---
url_co2 = 'https://gml.noaa.gov/webdata/ccgg/trends/co2/co2_mm_gl.txt'
response = requests.get(url_co2)
lines = response.text.splitlines()

average_co2 = []
for line in lines:
    if not line.startswith('%') and line.strip() != '':
        parts = line.split()
        try:
            average_co2.append(float(parts[3]))  # Kolonne 3 = Average
        except:
            pass

# --- Hent temperaturdata ---
url_temp = 'https://berkeley-earth-temperature.s3.us-west-1.amazonaws.com/Global/Land_and_Ocean_complete.txt'
response = requests.get(url_temp)
lines = response.text.splitlines()

temperature_anomalies = []
for line in lines:
    if not line.startswith('%') and line.strip() != '':
        parts = line.split()
        try:
            year = int(parts[0])
            month = int(parts[1])
            if year >= 1979 and year <= 2024:
                temperature_anomalies.append(float(parts[2]))
        except:
            pass

# --- Sørg for at listene har samme lengde ---
min_len = min(len(average_co2), len(temperature_anomalies))
co2 = np.array(average_co2[:min_len])
temp = np.array(temperature_anomalies[:min_len])

# --- Beregn kovarians og korrelasjon ---
covariance = np.cov(co2, temp)[0,1]
var_co2 = np.var(co2, ddof=1)
var_temp = np.var(temp, ddof=1)
correlation = covariance / np.sqrt(var_co2 * var_temp)
print(f'Korrelasjon mellom CO₂ og temperaturavvik: {correlation:.4f}')

# --- Lag scatter-plot ---
plt.figure(figsize=(8,6))
plt.scatter(co2, temp, s=10, color='blue', alpha=0.6,)

# Legg til lineær trendlinje
m, b = np.polyfit(co2, temp, 1)  # linær regresjon: temp ≈ m*CO2 + b
plt.plot(co2, m*co2 + b, color='purple', linewidth=2, label=f'Korrelasjon (r={correlation:.2f})')

plt.xlabel('CO₂ (ppm)')
plt.ylabel('Temperaturavvik (°C)')
plt.title('Korrelasjon mellom CO₂ og temperaturavvik (1979-2024)')
plt.legend()
plt.grid(True)
plt.show()
