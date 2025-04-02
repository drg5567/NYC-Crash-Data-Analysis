# Queries that were used for the analysis of this data

# Question 3
# Number of Crashes in June 2020 with Pedestrians injured and/or killed
SELECT COUNT(*) AS June_2020_Pedestrians
FROM crash_data
WHERE crash_date BETWEEN '2020-06-01' AND '2020-06-30'
  AND (number_of_pedestrians_injured > 0 OR number_of_pedestrians_killed > 0);

# Number of Crashes in June 2022 with Pedestrians injured and/or killed
SELECT COUNT(*) AS June_2022_Pedestrians
FROM crash_data
WHERE crash_date BETWEEN '2022-06-01' AND '2022-06-30'
  AND (number_of_pedestrians_injured > 0 OR number_of_pedestrians_killed > 0);

# Number of Crashes in June 2020 involving delivery vehicles
SELECT COUNT(*) AS June_2020_Delivery_Vehicles
FROM crash_data
WHERE crash_date BETWEEN '2020-06-01' AND '2020-06-30'
  AND (vehicle_type_code_1 = 'Delivery Vehicle' OR
       vehicle_type_code_2 = 'Delivery Vehicle' OR
       vehicle_type_code_3 = 'Delivery Vehicle' OR
       vehicle_type_code_4 = 'Delivery Vehicle' OR
       vehicle_type_code_5 = 'Delivery Vehicle');

# Number of Crashes in June 2022 involving delivery vehicles
SELECT COUNT(*) AS June_2022_Delivery_Vehicles
FROM crash_data
WHERE crash_date BETWEEN '2022-06-01' AND '2022-06-30'
  AND (vehicle_type_code_1 = 'Delivery Vehicle' OR
       vehicle_type_code_2 = 'Delivery Vehicle' OR
       vehicle_type_code_3 = 'Delivery Vehicle' OR
       vehicle_type_code_4 = 'Delivery Vehicle' OR
       vehicle_type_code_5 = 'Delivery Vehicle');

# Number of Crashes in June 2020 involving ambulances
SELECT COUNT(*) AS June_2020_Ambulances
FROM crash_data
WHERE crash_date BETWEEN '2020-06-01' AND '2020-06-30'
  AND (LOWER(vehicle_type_code_1) LIKE '%amb%' OR
       LOWER(vehicle_type_code_2) LIKE '%amb%' OR
       LOWER(vehicle_type_code_3) LIKE '%amb%' OR
       LOWER(vehicle_type_code_4) LIKE '%amb%' OR
       LOWER(vehicle_type_code_5) LIKE '%amb%');

# Number of Crashes in June 2022 involving ambulances
SELECT COUNT(*) AS June_2022_Ambulances
FROM crash_data
WHERE crash_date BETWEEN '2022-06-01' AND '2022-06-30'
  AND (LOWER(vehicle_type_code_1) LIKE '%amb%' OR
       LOWER(vehicle_type_code_2) LIKE '%amb%' OR
       LOWER(vehicle_type_code_3) LIKE '%amb%' OR
       LOWER(vehicle_type_code_4) LIKE '%amb%' OR
       LOWER(vehicle_type_code_5) LIKE '%amb%');

# Number of Crashes in June 2020 involving bikes
SELECT COUNT(*) AS June_2020_Bikes
FROM crash_data
WHERE crash_date BETWEEN '2020-06-01' AND '2020-06-30'
  AND (LOWER(vehicle_type_code_1) = 'bike' OR
       LOWER(vehicle_type_code_2) = 'bike' OR
       LOWER(vehicle_type_code_3) = 'bike' OR
       LOWER(vehicle_type_code_4) = 'bike' OR
       LOWER(vehicle_type_code_5) = 'bike');

# Number of Crashes in June 2022 involving bikes
SELECT COUNT(*) AS June_2022_Bikes
FROM crash_data
WHERE crash_date BETWEEN '2022-06-01' AND '2022-06-30'
  AND (LOWER(vehicle_type_code_1) = 'bike' OR
       LOWER(vehicle_type_code_2) = 'bike' OR
       LOWER(vehicle_type_code_3) = 'bike' OR
       LOWER(vehicle_type_code_4) = 'bike' OR
       LOWER(vehicle_type_code_5) = 'bike');


# Question 4
# Contributing factors for two vehicles for July 2020
SELECT contributing_factor_vehicle_1, contributing_factor_vehicle_2, COUNT(*)
FROM crash_data
WHERE crash_date BETWEEN '2020-07-01' AND '2020-07-31'
GROUP BY contributing_factor_vehicle_1, contributing_factor_vehicle_2
ORDER BY COUNT(*) DESC;

# Contributing factors for two vehicles for July 2022
SELECT contributing_factor_vehicle_1, contributing_factor_vehicle_2, COUNT(*)
FROM crash_data
WHERE crash_date BETWEEN '2022-07-01' AND '2022-07-31'
GROUP BY contributing_factor_vehicle_1, contributing_factor_vehicle_2
ORDER BY COUNT(*) DESC;

# Number of accidents that injured people during July 2020
SELECT COUNT(*) FROM crash_data
WHERE crash_date BETWEEN '2020-07-01' AND '2020-07-31'
AND number_of_persons_injured > 0;

# Number of accidents that injured people during July 2022
SELECT COUNT(*) FROM crash_data
WHERE crash_date BETWEEN '2022-07-01' AND '2022-07-31'
AND number_of_persons_injured > 0;

# Number of accidents that killed people during July 2020
SELECT COUNT(*) FROM crash_data
WHERE crash_date BETWEEN '2020-07-01' AND '2020-07-31'
AND number_of_persons_killed > 0;

# Full data of accidents that killed people in July 2020
SELECT * FROM crash_data
WHERE crash_date BETWEEN '2020-07-01' AND '2020-07-31'
AND number_of_persons_killed > 0;

# Number of accidents that killed people during July 2022
SELECT COUNT(*) FROM crash_data
WHERE crash_date BETWEEN '2022-07-01' AND '2022-07-31'
AND number_of_persons_killed > 0;


# Questions 6 and 7
SELECT DAYNAME(crash_date) AS Crash_Day, COUNT(*) AS Num_Crashes
FROM crash_data
GROUP BY Crash_Day
ORDER BY Num_Crashes DESC;


# Questions 8 and 9
SELECT DATE_FORMAT(crash_time, '%H') AS Hour, COUNT(*) AS Num_Crashes
FROM crash_data
WHERE crash_time BETWEEN '06:00:00' AND '12:59:59'
GROUP BY Hour
ORDER BY Num_Crashes DESC;


# Question 10
SELECT crash_date, COUNT(*) AS Num_Crashes
FROM crash_data
WHERE crash_date BETWEEN '2022-01-01' AND '2022-12-31'
GROUP BY crash_date
ORDER BY Num_Crashes DESC
LIMIT 10;

