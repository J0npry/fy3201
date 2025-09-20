import pandas as pd

# URL of the data file
url_metan = "https://gml.noaa.gov/webdata/ccgg/trends/ch4/ch4_mm_gl.txt"

# Read the file, skipping the header rows (first 61 lines are metadata)
metan = pd.read_csv(url_metan, sep = '\s+', skiprows=46)

metan.columns = ['year','month','decimal_date','ch4_average','ch4_average_unc','ch4_trend','ch4_trend_unc','unused']

# Display the first few rows
metan.head()

metan['year'].head(10)
