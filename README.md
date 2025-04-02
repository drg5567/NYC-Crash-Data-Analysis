# New York City Crash Data Analysis
Final project for CSCI 720: Big Data Analytics

## Project Overview
Data Mining was performed on car accident data from New York City public records,
data was focused on the borough of Brooklyn.
Data was stored in a MySQL Database contained in localhost.

The files in this project were used to answer the following questions regarding the data:
1. What ethical considerations are there? Suppose you find a neighborhood that has many accidents, and you publish this. Could you be
sued? Is it just data?
2. Pick two regions of time, say two years. Figure out what has changed from one year to the next.
Figure out how to visualize the difference, in some way.
3. How was June of 2020 different then June of 2022?
Figure out how to show or demonstrate the difference.
Were there more pedestrian accidents? Where there more accidents involving delivery vehicles?
4. How was July of 2020 different then July of 2022?
Figure out how to show or demonstrate the difference. What was the reported cause of the accidents?
5. For the year of January 2020 to October of 2022, which 60 consecutive days had the most accidents?
The Automobile Association of America (AAA) say they are in the summer. Can you verify this?
6. Which day of the week has the fewest accidents?
7. Which day of the week has the most accidents?
8. From 6 AM to 12PM, which hour of the day has the fewest accidents?
9. From 6 AM to 12PM, which hour of the day has the most accidents?
10. In the year 2022, which 10 days had the most accidents?
This is not consecutive days. For example are there more accidents before the December holidays?
Is this true? Can you speculate about why the worst days are the worst days?

## Run Project
### Prerequisites
Must have Python and MySQL installed on your system. The repository scripts utilize the
PyMySQL library to connect to the database.

### Setting up Database
Download the New York City Car Accident records from 
[here](https://data.cityofnewyork.us/Public-Safety/Motor-Vehicle-Collisions-Crashes/h9gi-nx95/about_data).

Create a database on your MySQL instance to store the records (example: "brooklyn_crashes").
Following this, you can run `table_creation.sql` to create the initial table on
your database.

Update `load_brooklyn_data.py` to include the connection information to the MySQL database
as well as the file path for where you downloaded the NYC crash data. Then run the script
to add the borough data. After this is completed, run
`data_cleaning.sql` to perform some final preparation of the data

### Running scripts
For any script you want to run, update the PyMySQL connection function to include the
account information and database name of your database. After this you can run the files
and view the outputted figures.