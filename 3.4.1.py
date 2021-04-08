import requests
import sys

API_KEY = '14EfzsWYiaU3tBzgizxA'

params = {
    'api_key': API_KEY,
    'start_date': '2016-12-30',
    'end_date': '2017-12-31'
}

# THE SPECIFIED DATASET IS NOT FREE
# CARL ZEISS MEDITEC DATA WAS UNAVAILABLE WITHOUT A PAID SUBSCRIPTION
# THE DATASET USED BELOW IS PROVIDED AS A FREE SAMPLE FROM THE DATABASE
QUANDL_CODE = 'AGB2_UADJ'

# TASK 1: COLLECT DATA
r = requests.get(f'https://www.quandl.com/api/v3/datasets/XFRA/{QUANDL_CODE}', params=params)

# TASK 2: CONVERT TO DICTIONARY
json = r.json()

# COLUMN LOOKUP
columnIndex = dict(zip(json['dataset']['column_names'], range(0, len(json['dataset']['column_names']))))

data = json['dataset']['data'][1:len(json['dataset']['data'])-1]


highest = 0
lowest = sys.maxsize
maxDeltaDailyHighLow = 0
prevClose = json['dataset']['data'][0][columnIndex['Close']]
maxDeltaDailyClose = 0
volumeSum = 0

for d in data:
    high = d[columnIndex['High']]
    low = d[columnIndex['Low']]
    close = d[columnIndex['Close']]

    # TASK 3: CALCULATE HIGHEST AND LOWEST OPENING PRICES
    highest = high if high > highest else highest
    lowest = low if low < lowest else lowest

    # TASK 4: LARGEST DELTA OF DAILY HIGH/LOW
    delta = high - low
    maxDeltaDailyHighLow = delta if delta > maxDeltaDailyHighLow else maxDeltaDailyHighLow

    # TASK 5: LARGEST DELTA OF DAILY CLOSE
    closeDelta = close - prevClose
    maxDeltaDailyClose = closeDelta if closeDelta > maxDeltaDailyClose else maxDeltaDailyClose

    volumeSum += d[columnIndex['Volume']]
    prevClose = close

# TASK 6: VOLUME AVERAGE
volumeAverage = volumeSum / len(data)

# TASK 7: MEDIAN VOLUME
ci = columnIndex['Volume']
volume = sorted(map(lambda d: d[ci], data))
vi = int(len(volume) / 2)
medianVolume = (volume[vi-1] + volume[vi]) / 2 if len(volume) % 2 == 0 else volume[vi]

print(f'highest: {highest}')
print(f'lowest: {lowest}')
print(f'maxDeltaDailyHighLow: {maxDeltaDailyHighLow}')
print(f'maxDeltaDailyClose: {maxDeltaDailyClose}')
print(f'volumeAverage: {volumeAverage}')
print(f'medianVolume: {medianVolume}')
