import pymysql
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

conn = pymysql.connect(host='localhost', user='root', password='w00dlandAllianc3', db="brooklyn_crashes")
cur = conn.cursor()

sql_stmt = ("SELECT ROUND(latitude, 3) AS lat, ROUND(longitude, 3) AS longit, COUNT(*) AS Num_Crashes "
            "FROM crash_data "
            "WHERE latitude <= 40.76 AND longitude <= -73.8 "
            "GROUP BY lat, longit "
            "ORDER BY Num_Crashes DESC")

print("Executing SQL Statement:")
cur.execute(sql_stmt)
results = cur.fetchall()

print("Building Dataframe:")
crash_df = pd.DataFrame(results, columns=['latitude', 'longitude', 'num_crashes'])

print("Building Heatmap:")
plt.figure(figsize=(7, 8))
sns.heatmap(data=crash_df.pivot_table(index="latitude", columns="longitude", values="num_crashes"), cmap="YlOrRd")
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.title('Brooklyn Crashes Heatmap by Latitude and Longitude')

plt.savefig("brooklyn_crash_heatmap.png")
