import csv
import matplotlib.pyplot as plt
from datetime import datetime
from collections import defaultdict
import numpy as np
from scipy.stats import linregress

# === Data containers ===
dates = []
precipitation = []
month_data = defaultdict(list)

# === Read CSV ===
with open('nedborRennesoy.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=';')
    for row in reader:
        date_str = row['Tid(norsk normaltid)'].strip()
        precip_str = row['Nedbør (mnd)'].strip()
        if not date_str or not precip_str:
            continue
        
        # Parse date and precipitation
        date = datetime.strptime(date_str, '%m.%Y')
        prec_value = float(precip_str.replace(',', '.'))
        dates.append(date)
        precipitation.append(prec_value)
        
        # Group by month for normals
        month = int(date_str.split('.')[0])
        month_data[month].append(prec_value)

# === Normal monthly precipitation ===
normal_precipitation = {m: sum(vals)/len(vals) for m, vals in month_data.items()}

print("\n=== Normal Monthly Precipitation (mm) ===")
for month in range(1, 13):
    print(f"Month {month:02d}: {normal_precipitation.get(month, 0):.2f} mm")

# === Wettest & driest months ===
wettest_month = max(normal_precipitation, key=normal_precipitation.get)
driest_month = min(normal_precipitation, key=normal_precipitation.get)
print(f"\nWettest month: {wettest_month:02d} ({normal_precipitation[wettest_month]:.2f} mm)")
print(f"Driest month: {driest_month:02d} ({normal_precipitation[driest_month]:.2f} mm)")

# === Climatologically drier months ===
annual_mean = sum(normal_precipitation.values()) / len(normal_precipitation)
print(f"\nAnnual mean precipitation: {annual_mean:.2f} mm")
print("Drier months than average:")
for m, avg in normal_precipitation.items():
    if avg < annual_mean:
        print(f"  Month {m:02d}: {avg:.2f} mm")

# === Trend analysis ===
x = np.array([d.toordinal() for d in dates])  # numeric dates
y = np.array(precipitation)

coeffs = np.polyfit(x, y, 1)  # slope, intercept
trendline = np.poly1d(coeffs)
print(f"\nTrend slope: {coeffs[0]:.6f} mm per day "
      f"({coeffs[0]*365:.2f} mm per year)")

# === Expected values (normal for each month) ===
expected_precip = [normal_precipitation[d.month] for d in dates]

# === Plot 2: Precipitation trend with normals ===
plt.figure(figsize=(10, 5))
plt.plot(dates, precipitation, marker='o', linestyle='-', label='Observert')
plt.plot(dates, trendline(x), color='red', linewidth=2, label='Trend for observert data')
plt.scatter(dates, expected_precip, color='green', marker='o', label="forventet Månedlig")
plt.title('Nedbør over tid - Rennesøy (med trend)')
plt.xlabel('Dato')
plt.ylabel('Nedbør (mm)')
plt.legend()
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Linear regression with significance test
slope, intercept, r_value, p_value, std_err = linregress(x, y)

print("\n=== Trend Analysis ===")
print(f"Slope: {slope:.6f} mm per day ({slope*365:.2f} mm per year)")
print(f"R-squared: {r_value**2:.3f}")
print(f"P-value: {p_value:.4f}")

if p_value < 0.05:
    print("➡️ The trend IS statistically significant (95% confidence) with p = .",p_value)
else:
    print("➡️ The trend is NOT statistically significant with p = .",p_value)