import datetime

# Define the latitude, longitude, and time interval (1 hour interval)
lat = 36.1889
lon = -75.9
time_interval = datetime.timedelta(seconds=10)  # 1 hour interval

# Define start and end times
start_time = datetime.datetime(1994, 10, 12, 17, 0, 0)
end_time = datetime.datetime(1994, 10, 12, 21, 0, 0)

# Open the file to write
with open('lat_lon_time_Duck', 'w') as fid:
    current_time = start_time
    while current_time <= end_time:
        # Write the data to the file in the required format
        fid.write(f'{lat:10.4f} {lon:10.4f} {current_time.year:8d} {current_time.month:4d} '
                  f'{current_time.day:4d} {current_time.hour:4d} {current_time.minute:4d} '
                  f'{current_time.second:4d}\n')
        # Increment time by 1 hour
        current_time += time_interval
