# -*- coding: utf-8 -*-
"""proj.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ZQZcEHmTeA2ozNG0gHTupEei6eeRPQW5
"""

from google.colab import drive
drive.mount('/content/drive')

import pandas as pd
import geopy.distance
from datetime import datetime, timedelta


df = pd.read_csv(io.BytesIO(uploaded['example.csv']))
#df_dd['id'] = df_dd.reset_index().index

df_t = pd.DataFrame({
    'person_id': df['person_id'],
    'time_stamp': list(
        map(lambda x: datetime.strptime(x, '%Y/%m/%d %H:%M:%S.%f'),
            df['time_stamp_milliseconds'])),
    'x': df['x'].astype(float),
    'y': df['y'].astype(float),
    'id': df['id'],
})

user_12 = df_t[df_t['person_id'] == 'Grp20220712.12.1']
user_15 = df_t[df_t['person_id'] == 'Grp20220712.15.1']
user_21 = df_t[df_t['person_id'] == 'Grp20220712.21.1']
user_27 = df_t[df_t['person_id'] == 'Grp20220712.27.1']
user_28 = df_t[df_t['person_id'] == 'Grp20220712.28.1']

import geopy.distance
from datetime import datetime, timedelta
import math

avgSpeeds = [0.69496854618901,
             0.70978878,
             0.7097887883268266,
             0.6448299921524852,
             0.6836773630752111]


medSpeeds = [0.4858241588715713, 0.4648084434550697, 0.3420983714514612, 0.4317949123485175, 0.43171787337066964]
combSpeeds = list(map(lambda x: sum(x) / len(x), zip(avgSpeeds, medSpeeds)))

def calculate_staypoints(present_user, dist_limit, time_limit):
    stop_points = []
    i = 0
    m = len(present_user)
    print(m)

    while i < m - 1:
        j = i + 1
        while j < m:
            point_i = present_user.iloc[i]
            point_j = present_user.iloc[j]
            dist = math.sqrt(
                (point_j['x'] - point_i['x'])**2 +
                (point_j['y'] - point_i['y'])**2
                )
            if dist > dist_limit:
                tspan = abs((point_j['time_stamp'] -
                             point_i['time_stamp']).total_seconds())
                if tspan > time_limit:
                    lat_mean = present_user.iloc[i:j-1]['x'].mean()
                    lon_mean = present_user.iloc[i:j-1]['y'].mean()
                    stop_points.append({
                        'lat' : lat_mean,
                        'lon' : lon_mean,
                        'start_ts' : point_i['time_stamp'],
                        'end_ts' : point_j['time_stamp'],
                        'size' : j - i,
                        'range' : [point_i.id, point_j.id],
                        'tspan' : tspan,
                        'dist' : dist,
                        'speed' : dist/tspan,
                        'id' : point_i.id,
                    })
                i = j
                break
            j += 1
        i += 1

    return stop_points

# Define the user and the distance and time limits
present_user = user_12
x = avgSpeeds[0]
distLimCm = 1
timeLimSec = (1 + x**2)/x
# timeLimSec = 1.7/avgSpeeds[0]
stop_points_o = calculate_staypoints(present_user, distLimCm, timeLimSec)

print((stop_points_o))
print(len(stop_points_o))

import csv

def save_staypoints_to_csv(staypoints, filename):
    fieldnames = ['lat', 'lon', 'start_ts', 'end_ts', 'size', 'range', 'tspan','dist', 'speed', 'id']
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(stop_points_o)

# Assuming you have the 'staypoints' list of dictionaries
save_staypoints_to_csv(stop_points_o, 'present12.csv')