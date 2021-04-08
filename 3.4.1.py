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
column_index = dict(zip(json['dataset']['column_names'], range(0, len(json['dataset']['column_names']))))

data = json['dataset']['data'][1:len(json['dataset']['data'])-1]


highest = 0
lowest = sys.maxsize
max_delta_daily_high_low = 0
prev_close = json['dataset']['data'][0][column_index['Close']]
max_delta_daily_close = 0
volume_sum = 0

for d in data:
    high = d[column_index['High']]
    low = d[column_index['Low']]
    close = d[column_index['Close']]

    # TASK 3: CALCULATE HIGHEST AND LOWEST OPENING PRICES
    highest = high if high > highest else highest
    lowest = low if low < lowest else lowest

    # TASK 4: LARGEST DELTA OF DAILY HIGH/LOW
    delta = high - low
    max_delta_daily_high_low = delta if delta > max_delta_daily_high_low else max_delta_daily_high_low

    # TASK 5: LARGEST DELTA OF DAILY CLOSE
    close_delta = close - prev_close
    max_delta_daily_close = close_delta if close_delta > max_delta_daily_close else max_delta_daily_close

    volume_sum += d[column_index['Volume']]
    prev_close = close

# TASK 6: VOLUME AVERAGE
volume_average = volume_sum / len(data)

# TASK 7: MEDIAN VOLUME
ci = column_index['Volume']
volume = sorted(map(lambda d: d[ci], data))
vi = int(len(volume) / 2)
median_volume = (volume[vi-1] + volume[vi]) / 2 if len(volume) % 2 == 0 else volume[vi]

print(f'highest: {highest}')
print(f'lowest: {lowest}')
print(f'max_delta_daily_high_low: {max_delta_daily_high_low}')
print(f'max_delta_daily_close: {max_delta_daily_close}')
print(f'volume_average: {volume_average}')
print(f'median_volume: {median_volume}')
