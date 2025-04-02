/*
########## DATA CLEANING ##############
Performs some small data cleaning on the data table

Author: Danny Gardner
 */
UPDATE crash_data
SET vehicle_type_code_1 = 'Delivery Vehicle'
WHERE LOWER(vehicle_type_code_1) LIKE '%del%'
   OR LOWER(vehicle_type_code_1) LIKE '%livery%';

UPDATE crash_data
SET vehicle_type_code_2 = 'Delivery Vehicle'
WHERE LOWER(vehicle_type_code_2) LIKE '%del%'
   OR LOWER(vehicle_type_code_2) LIKE '%livery%';

UPDATE crash_data
SET vehicle_type_code_3 = 'Delivery Vehicle'
WHERE LOWER(vehicle_type_code_3) LIKE '%del%'
   OR LOWER(vehicle_type_code_3) LIKE '%livery%';

UPDATE crash_data
SET vehicle_type_code_4 = 'Delivery Vehicle'
WHERE LOWER(vehicle_type_code_4) LIKE '%del%'
   OR LOWER(vehicle_type_code_4) LIKE '%livery%';

UPDATE crash_data
SET vehicle_type_code_5 = 'Delivery Vehicle'
WHERE LOWER(vehicle_type_code_5) LIKE '%del%'
   OR LOWER(vehicle_type_code_5) LIKE '%livery%';
