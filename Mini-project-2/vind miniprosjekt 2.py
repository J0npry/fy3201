import csv
import os
import numpy as np
from matplotlib import pyplot as plt

def read_csv(file_name: str):
    file_path = file_name
    with open(file_path, mode='r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')  
        data = [[cell.replace(',', '.') for cell in row] for row in reader]
    return np.array(data)[1:-1]

data = read_csv('vindSogndal.csv')

dates = data[:,2] 
max_temps = np.array(data[:,3])

def convert_to_float(arr):
    result = []
    for val in arr:
        if val.strip() == '-' or val.strip() == '':  
            result.append(np.nan)  # NaN for manglende verdier
        else:
            result.append(float(val))
    return np.array(result, dtype=float)

max_temps = convert_to_float(max_temps)

new_data = np.column_stack((dates, max_temps))
sorted_idx = np.argsort(new_data[:, 0])
new_data_sorted = new_data[sorted_idx]

avrg_max_temp_by_month = []

max_temp_month_map = {1:np.array([]), 2:np.array([]), 3:np.array([]), 4:np.array([]), 5:np.array([]), 6:np.array([]), 7:np.array([]), 8:np.array([]), 9:np.array([]), 10:np.array([]), 11:np.array([]), 12:np.array([])}

for i in range(len(new_data_sorted)):
    month = int(new_data_sorted[i, 0][:2]) 
    max_val = float(new_data_sorted[i, 1])

    if not np.isnan(max_val):
        max_temp_month_map[month] = np.append(max_temp_month_map[month], max_val)
for i in range(1, 13):
    avrg_max_temp_by_month.append(float(np.average(max_temp_month_map[i])))



plt.plot(range(1, 13), avrg_max_temp_by_month, label='Gjennomsnittlig månedlig middelvind 1994-2024', marker='o', color='red')
plt.xticks(range(1, 13), ['Jan', 'Feb', 'Mar', 'Apr', 'Mai', 'Jun', 'Jul', 'Aug', 'Sep', 'Okt', 'Nov', 'Des'])
plt.xlabel('Måned')
plt.ylabel('Temperatur (C)')
plt.title('Høyeste månedlig middelvind')
plt.grid()
dara_2025 = read_csv('vindSogndal2025.csv') #hent 2025 data
dates_2025 = dara_2025[:,2]
max_temps_2025 = convert_to_float(dara_2025[:,3])
plt.plot(range(1, len(max_temps_2025)+1), max_temps_2025, label='Høyeste månedlig middelvind 2025', marker='o', linestyle='--', color='orange')

plt.legend()
plt.show()
