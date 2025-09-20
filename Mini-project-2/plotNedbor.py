import csv
import matplotlib.pyplot as plt
from datetime import datetime

# Lists to store the data
dates = []
precipitation = []

# Open the CSV file
with open('nedborRennesoy.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=';')  # Use ; as separator
    for row in reader:
        date_str = row['Tid(norsk normaltid)'].strip()  # remove whitespace
        if not date_str:  # skip empty strings
            continue
        date = datetime.strptime(date_str, '%m.%Y')
        dates.append(date)
        precipitation.append(float(row['Nedbør (mnd)'].replace(',', '.')))

# Plotting
plt.figure(figsize=(10, 5))
plt.plot(dates, precipitation, marker='o', linestyle='-')
plt.title('Månedlig nedbør - Rennesøy')
plt.xlabel('Date')
plt.ylabel('Nedbør (mm)')
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
