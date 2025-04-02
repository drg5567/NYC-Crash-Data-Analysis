# Initial table creation and data cleaning

CREATE TABLE crash_data
(
    collision_id                  int,
    crash_date                    date,
    crash_time                    time,
    zip_code                      int,
    latitude                      double,
    longitude                     double,
    location                      varchar(50),
    on_street_name                varchar(75),
    cross_street_name             varchar(75),
    off_street_name               varchar(75),
    number_of_persons_injured     int,
    number_of_persons_killed      int,
    number_of_pedestrians_injured int,
    number_of_pedestrians_killed  int,
    number_of_cyclists_injured    int,
    number_of_cyclists_killed     int,
    number_of_motorist_injured    int,
    number_of_motorist_killed     int,
    contributing_factor_vehicle_1 varchar(100),
    contributing_factor_vehicle_2 varchar(100),
    contributing_factor_vehicle_3 varchar(100),
    contributing_factor_vehicle_4 varchar(100),
    contributing_factor_vehicle_5 varchar(100),
    vehicle_type_code_1           varchar(50),
    vehicle_type_code_2           varchar(50),
    vehicle_type_code_3           varchar(50),
    vehicle_type_code_4           varchar(50),
    vehicle_type_code_5           varchar(50)
);

########## DATA CLEANING ##############
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
