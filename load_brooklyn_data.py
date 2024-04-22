import pymysql
import pandas as pd
import numpy as np
import datetime

"""
Loads the initial data for the database from a CSV file downloaded from the NYC traffic authority

@author: Danny Gardner      drg5567
"""


def reformat_date(date_str):
    return datetime.datetime.strptime(date_str, '%m/%d/%Y').strftime('%Y-%m-%d')


conn = pymysql.connect(host='localhost', user='root', password='w00dlandAllianc3', db="brooklyn_crashes")
cur = conn.cursor()

print("Reading Data From CSV")
crash_data = pd.read_csv("C:\\Users\\Public\\Documents\\nyc_data\\Motor_Vehicle_Collisions_-_Crashes_20240416.csv")
print("Cleaning Data")
crash_data = crash_data.replace({np.nan: None})

insert_stmt = "INSERT INTO crash_data(collision_id,\
    crash_date,\
    crash_time,\
    zip_code,\
    latitude,\
    longitude,\
    location,\
    on_street_name,\
    cross_street_name,\
    off_street_name,\
    number_of_persons_injured,\
    number_of_persons_killed,\
    number_of_pedestrians_injured,\
    number_of_pedestrians_killed,\
    number_of_cyclists_injured,\
    number_of_cyclists_killed,\
    number_of_motorist_injured,\
    number_of_motorist_killed,\
    contributing_factor_vehicle_1,\
    contributing_factor_vehicle_2,\
    contributing_factor_vehicle_3,\
    contributing_factor_vehicle_4,\
    contributing_factor_vehicle_5,\
    vehicle_type_code_1,\
    vehicle_type_code_2,\
    vehicle_type_code_3,\
    vehicle_type_code_4,\
    vehicle_type_code_5) \
    VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

print("Inserting Brooklyn Data into Database")
record_count = 0
for i in range(len(crash_data)):
    row = crash_data.loc[i]
    if row["BOROUGH"] == "BROOKLYN":
        if record_count % 500 == 0:
            print("Inserting Record " + str(record_count))
        crash_date = reformat_date(row["CRASH DATE"])
        cur.execute(insert_stmt,
                    [row["COLLISION_ID"],
                     crash_date,
                     row["CRASH TIME"],
                     row["ZIP CODE"],
                     row["LATITUDE"],
                     row["LONGITUDE"],
                     row["LOCATION"],
                     row["ON STREET NAME"],
                     row["CROSS STREET NAME"],
                     row["OFF STREET NAME"],
                     row["NUMBER OF PERSONS INJURED"],
                     row["NUMBER OF PERSONS KILLED"],
                     row["NUMBER OF PEDESTRIANS INJURED"],
                     row["NUMBER OF PEDESTRIANS KILLED"],
                     row["NUMBER OF CYCLIST INJURED"],
                     row["NUMBER OF CYCLIST KILLED"],
                     row["NUMBER OF MOTORIST INJURED"],
                     row["NUMBER OF MOTORIST KILLED"],
                     row["CONTRIBUTING FACTOR VEHICLE 1"],
                     row["CONTRIBUTING FACTOR VEHICLE 2"],
                     row["CONTRIBUTING FACTOR VEHICLE 3"],
                     row["CONTRIBUTING FACTOR VEHICLE 4"],
                     row["CONTRIBUTING FACTOR VEHICLE 5"],
                     row["VEHICLE TYPE CODE 1"],
                     row["VEHICLE TYPE CODE 2"],
                     row["VEHICLE TYPE CODE 3"],
                     row["VEHICLE TYPE CODE 4"],
                     row["VEHICLE TYPE CODE 5"]])
        record_count += 1

conn.commit()
cur.close()
conn.close()
