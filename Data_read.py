import csv
import os
import numpy as np
from matplotlib import pyplot as plt
def read_csv(file_name: str):
    file_path = os.path.join(os.path.dirname(__file__), file_name)
    with open(file_path, mode='r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')  
        data = [row for row in reader]
    return np.array(data)[1:-1]

data = read_csv('Jonas_1994-2024.csv')

dates = data[:,2] 
max_temps = np.array(data[:,3])
min_temps = np.array(data[:,4])

def convert_to_float(arr):
    result = []
    for val in arr:
        if val.strip() == '-' or val.strip() == '':  
            result.append(np.nan)  # NaN for manglende verdier
        else:
            result.append(float(val))
    return np.array(result, dtype=float)

max_temps = convert_to_float(max_temps)
min_temps = convert_to_float(min_temps)

new_data = np.column_stack((dates, min_temps, max_temps))
sorted_idx = np.argsort(new_data[:, 0])
new_data_sorted = new_data[sorted_idx]
avrg_min_temp_by_month = []
avrg_max_temp_by_month = []
min_temp_month_map = {1:np.array([]), 2:np.array([]), 3:np.array([]), 4:np.array([]), 5:np.array([]), 6:np.array([]), 7:np.array([]), 8:np.array([]), 9:np.array([]), 10:np.array([]), 11:np.array([]), 12:np.array([])}
max_temp_month_map = {1:np.array([]), 2:np.array([]), 3:np.array([]), 4:np.array([]), 5:np.array([]), 6:np.array([]), 7:np.array([]), 8:np.array([]), 9:np.array([]), 10:np.array([]), 11:np.array([]), 12:np.array([])}

for i in range(len(new_data_sorted)):
    month = int(new_data_sorted[i, 0][:2]) 
    min_val = float(new_data_sorted[i, 1])
    max_val = float(new_data_sorted[i, 2])
    if not np.isnan(min_val):
        min_temp_month_map[month] = np.append(min_temp_month_map[month], min_val)
    if not np.isnan(max_val):
        max_temp_month_map[month] = np.append(max_temp_month_map[month], max_val)
print(max_temp_month_map[7])
for i in range(1, 13):
    avrg_min_temp_by_month.append(float(np.average(min_temp_month_map[i])))
    avrg_max_temp_by_month.append(float(np.average(max_temp_month_map[i])))


plt.plot(range(1, 13), avrg_min_temp_by_month, label='Gjennomsnittlig minimumstemperatur', marker='o')
plt.plot(range(1, 13), avrg_max_temp_by_month, label='Gjennomsnittlig maksimumstemperatur', marker='o')
plt.xticks(range(1, 13), ['Jan', 'Feb', 'Mar', 'Apr', 'Mai', 'Jun', 'Jul', 'Aug', 'Sep', 'Okt', 'Nov', 'Des'])
plt.xlabel('Måned')
plt.ylabel('Temperatur (C)')
plt.title('Gjennomsnittlig månedlig minimums- og maksimumstemperatur (1994-2024)')
plt.legend()
plt.grid()
plt.show()