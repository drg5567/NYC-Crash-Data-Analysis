import pymysql
import pandas as pd
import matplotlib.pyplot as plt

conn = pymysql.connect(host='localhost', user='root', password='w00dlandAllianc3', db="brooklyn_crashes")
cur = conn.cursor()


def parzen_graph(dataframe):
    """
    This function takes the dataframe used for the histogram and uses it to calculate parzen density estimations.
    First the dataset is normalized to estimate the probability of an event happening on a given day
    :param dataframe: The dataframe containing the number of events that occured for 70 days
    :return: None
    """
    # Normalize the graph
    total_events = dataframe["NumberOfEvents"].sum()
    # convert the NumberOfEvents column to floats so the data can be normalized
    convert_dict = {"Week": int, "NumberOfEvents": float}
    dataframe = dataframe.astype(convert_dict)

    for i in range(dataframe.shape[0]):
        dataframe.at[i, "NumberOfEvents"] = dataframe.at[i, "NumberOfEvents"] / total_events

    # Smooth over values with Gaussian kernel [.06 .12 .20 .24 .20 .12 .06]
    kernel = [.06, .12, .20, .24, .20, .12, .06]
    output_df = pd.DataFrame(columns=["Week", "Likelihood"])

    for day in range(dataframe.shape[0]):
        total = 0
        for k_idx in range(len(kernel)):
            k_factor = kernel[k_idx]
            data_idx = day + k_idx - 3
            data_to_scale = 0
            if data_idx >= 0 and data_idx < dataframe.shape[0]:
                data_to_scale = dataframe.at[data_idx, "NumberOfEvents"]
            temp = k_factor * data_to_scale
            total += temp
        row = {"Week": day, "Likelihood": total}
        output_df.loc[len(output_df)] = row

    # Generate graph of parzen density estimation
    output_df.plot(x="Week", y="Likelihood", title="Brooklyn Crash Parzen Density Estimation (Jan 2020 - Oct 2022)",
                   ylabel="Estimated Likelihood of Crash Per Week")
    plt.savefig("brooklyn_parzen_density.png")
    return


def clean_dataset(dataframe):
    binned_df = pd.DataFrame(columns=["Week", "NumberOfEvents"])
    for i in range(len(dataframe)):
        dataframe.at[i, "Day"] = i + 1

    week_count = 0
    for x in range(0, len(dataframe), 7):
        rows_left = len(dataframe) - x
        if rows_left >= 7:
            num_events = dataframe.iloc[x:x + 7, 1:2].sum().iloc[0]
        else:
            num_events = dataframe.iloc[x:x + rows_left, 1:2].sum().iloc[0]
        row = {"Week": week_count, "NumberOfEvents": num_events}
        binned_df.loc[len(binned_df)] = row
        week_count += 1

    return binned_df


#################################################################################################
sql_stmt = ("SELECT crash_date AS 'Day', COUNT(*) AS 'NumberOfEvents' "
            "FROM crash_data "
            "WHERE crash_date BETWEEN '2020-01-01' AND '2022-10-31' "
            "GROUP BY crash_date "
            "ORDER BY crash_date;")

print("Executing SQL")
cur.execute(sql_stmt)
results = cur.fetchall()
columns = [desc[0] for desc in cur.description]

crash_df = pd.DataFrame(results, columns=columns)

cleaned_crash_df = clean_dataset(crash_df.copy())

print("Generating Histogram")
hist = cleaned_crash_df.plot.bar(x="Week", y="NumberOfEvents", figsize=(22, 5),
                                 title="Number of Crashes in Brooklyn from Jan 2020 to Oct 2022", ylabel="Count")
plt.savefig("brooklyn_crash_histogram.png")

print("Generating Parzen Density Estimation")
# parzen density graphs
parzen_graph(cleaned_crash_df)

print("Finding Window:")
rolling_sum = crash_df['NumberOfEvents'].rolling(window=60).sum()
max_period_start_index = rolling_sum.idxmax()

# Extract the 60-day period with the most accidents
most_accidents_period = crash_df.iloc[max_period_start_index - 59:max_period_start_index + 1]
print("60-day period with the most accidents:")
print(most_accidents_period)

max_week_start = (max_period_start_index - 59) // 7
max_week_end = max_period_start_index // 7
print("\nThe most accidents occurred between weeks " + str(max_week_start) + " and " + str(max_week_end))
