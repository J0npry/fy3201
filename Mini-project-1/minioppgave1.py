import pandas
import matplotlib.pyplot as plt

url = "https://berkeley-earth-temperature.s3.us-west-1.amazonaws.com/Global/Land_and_Ocean_complete.txt"
dataFrame = pandas.read_csv(url, comment = "%", sep="\s+", header= None) #read csv with whitespace as seperator and ignores comments

#make headers for the corresponding collumn
columnNames = ["Year", "Month",
    "MonthlyAnomaly", "MonthlyUncertainty",
    "AnnualAnomaly", "AnnualUncertainty",
    "FiveYearAnomaly", "FiveYearUncertainty",
    "TenYearAnomaly", "TenYearUncertainty",
    "TwentyYearAnomaly", "TwentyYearUncertainty"
]
dataFrame.columns = columnNames[:len(dataFrame.columns)] #give the names directly to the data frame
dataFrame["Date"] = pandas.to_datetime(dict(year=dataFrame["Year"], month=dataFrame["Month"], day=1))#make so plt can have time on x-axis

#because there are two datasets, we need to find where the second one is
newDataBeginIndex = dataFrame[dataFrame["Year"] == 1850].index.tolist()
newDataBeginIndex = newDataBeginIndex[len(newDataBeginIndex)//2]# this is the index where it loops

#this loop plots all the properties of the climatedata remember all air data is before newDataBeginIndec hence the slicing.++
for i in range (2,12,2):
    property = dataFrame.columns[i]
    propertyUncertainty = dataFrame.columns[i + 1]

    plt.plot(dataFrame["Date"][:newDataBeginIndex], dataFrame[property][:newDataBeginIndex], label = property)

    #this makes the uncertainty shading
    plt.fill_between(
    dataFrame["Date"][:newDataBeginIndex],
    dataFrame[property][:newDataBeginIndex] - dataFrame[propertyUncertainty][:newDataBeginIndex],
    dataFrame[property][:newDataBeginIndex] + dataFrame[propertyUncertainty][:newDataBeginIndex],
    alpha=0.2
    )

plt.legend()
plt.title("Global Average Temperature Anomaly with Sea Ice Temperature Inferred from Air Temperatures")
plt.xlabel("year")
plt.ylabel("temp in °C")
plt.grid()
plt.show()



# Now we do the exact same but for water Temperatures
for i in range (2,12,2):
    property = dataFrame.columns[i]
    propertyUncertainty = dataFrame.columns[i + 1]

    plt.plot(dataFrame["Date"][newDataBeginIndex:], dataFrame[property][newDataBeginIndex:], label = property)

    #this makes the uncertainty shading
    plt.fill_between(
    dataFrame["Date"][newDataBeginIndex:],
    dataFrame[property][newDataBeginIndex:] - dataFrame[propertyUncertainty][newDataBeginIndex:],
    dataFrame[property][newDataBeginIndex:] + dataFrame[propertyUncertainty][newDataBeginIndex:],
    alpha=0.2
    )

plt.legend()
plt.title("Global Average Temperature Anomaly with Sea Ice Temperature Inferred from Water Temperatures")
plt.xlabel("year")
plt.ylabel("temp in °C")
plt.grid()
plt.show()




