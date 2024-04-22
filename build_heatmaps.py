import pymysql
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

"""
This script builds a heatmap of traffic data that occurs during 2019 and 2023 based on latitude and longitude

@author: Danny Gardner      drg5567
"""

conn = pymysql.connect(host='localhost', user='root', password='w00dlandAllianc3', db="brooklyn_crashes")
cur = conn.cursor()


def make_heatmap(year):
    """
    Generates a heatmap based on Brooklyn traffic data from a given year
    :param year: the year to gather data for
    :return: None
    """
    # Get the data to be used
    year_str = str(year)
    sql_stmt = ("SELECT ROUND(latitude, 3) AS lat, ROUND(longitude, 3) AS longit, COUNT(*) AS Num_Crashes "
                "FROM crash_data "
                "WHERE crash_date BETWEEN '" + year_str + "-01-01' AND '" + year_str + "-12-31' "
                "AND latitude > 0 and longitude < 0 "
                "GROUP BY lat, longit "
                "ORDER BY Num_Crashes DESC;")

    print("Executing SQL")
    cur.execute(sql_stmt)
    results = cur.fetchall()

    print("Building Heatmap")
    crash_df = pd.DataFrame(results, columns=['latitude', 'longitude', 'num_crashes'])

    plt.figure(figsize=(7, 8))
    sns.heatmap(data=crash_df.pivot_table(index="latitude", columns="longitude", values="num_crashes"), cmap="YlOrRd")
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.title('Brooklyn Crashes During ' + year_str)

    plt.savefig("brooklyn_crash_heatmap_ " + year_str + ".png")


#############################################################################
print("Building Heatmap of Brooklyn Traffic in 2019")
make_heatmap(2019)

print("Building Heatmap of Brooklyn Traffic in 2023")
make_heatmap(2023)

cur.close()
conn.close()
