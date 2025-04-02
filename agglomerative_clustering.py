import pymysql
import pandas as pd
from sklearn.cluster import AgglomerativeClustering
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import dendrogram, linkage

"""
This program performs agglomerative clustering on Brooklyn traffic data for accidents that occurred
during 2019 and 2023 respectively

Answers question 2 of project questions

@author: Danny Gardner      drg5567
"""

# Insert connection information in order to run script
conn = pymysql.connect(host='localhost', user='', password='', db="")
cur = conn.cursor()


def format_date(date):
    """
    Formats a datetime to a string
    :param date: the datetime
    :return: the formatted date
    """
    return date.strftime('%Y-%m-%d')


def gen_dataframe(year_str):
    """
    Select data from the database and construct the dataframe for future calculations
    :param year_str: the year of data to be extracted
    :return: the dataframe
    """
    sql_stmt = ("SELECT * FROM crash_data "
                "WHERE crash_date BETWEEN '" + year_str + "-01-01' AND '" + year_str + "-12-31' ")
    cur.execute(sql_stmt)
    results = cur.fetchall()
    columns = [desc[0] for desc in cur.description]

    df = pd.DataFrame(results, columns=columns)

    # Clean the numeric data columns
    df["zip_code"] = df["zip_code"].fillna(0)
    df["latitude"] = df["latitude"].fillna(0)
    df["longitude"] = df["longitude"].fillna(0)

    df["latitude"] = df["latitude"].round(3)
    df["longitude"] = df["longitude"].round(3)

    # format the date and time columns
    df["crash_date"] = df["crash_date"].apply(format_date)
    df["crash_time"] = df["crash_time"].astype(str).str[7:]

    string_cols = ["crash_date", "crash_time", "location", "on_street_name", "cross_street_name", "off_street_name",
                   "contributing_factor_vehicle_1", "contributing_factor_vehicle_2", "contributing_factor_vehicle_3",
                   "contributing_factor_vehicle_4", "contributing_factor_vehicle_5", "vehicle_type_code_1",
                   "vehicle_type_code_2", "vehicle_type_code_3", "vehicle_type_code_4", "vehicle_type_code_5"]

    # Encode the string columns as integers
    for col in string_cols:
        df[col] = df[col].astype('category').cat.codes

    return df


def gen_cross_corr_matrix(dataframe):
    """
    Generates a cross correlation matrix from a dataset
    :param dataframe: the dataframe of raw data
    :return: the matrix
    """
    df_copy = dataframe.drop(columns=["collision_id"])
    cross_corr_matrix = df_copy.corr().round(decimals=2)

    return cross_corr_matrix


def agglomerative_clustering(dataframe):
    """
    Calls agglomerative clustering on the dataframe using the sklearn library
    :param dataframe: the dataframe to use
    :return: The clustered data
    """
    cluster = AgglomerativeClustering(n_clusters=5, metric="euclidean", linkage='single')
    clusters = cluster.fit_predict(dataframe)

    # Add cluster labels to DataFrame
    dataframe['cluster'] = clusters
    return dataframe


def gen_dendrogram(dataframe, year_str):
    """
    Generates and saves a dendrogram of the dataset with the last 20 clusters
    :param dataframe: the original data
    :param year_str: the year of the dataset
    :return: None
    """
    linked = linkage(dataframe)
    plt.figure(figsize=(12, 5))
    dendrogram(linked, orientation='top', truncate_mode='lastp', p=20, distance_sort='descending',
               show_leaf_counts=True)
    plt.title('Brooklyn Crashes from ' + year_str + ' Dendrogram')
    plt.xlabel('Cluster Index')
    plt.ylabel('Distance')
    plt.savefig("brooklyn_dendrogram_" + year_str + ".png")
    return


def find_none_vals(crash_df):
    """
    Finds columns that have null values
    :param crash_df: the given dataframe
    :return: a list of columns with null values
    """
    none_cols = []
    for col in crash_df.columns:
        if crash_df[col].isna().any():
            none_cols.append(col)
    return none_cols


def agglo_functions(year_str):
    """
    The main function to perform all functions for agglomerative clustering
    :param year_str: the year to perform the functions on
    :return: None
    """
    print("Performing Agglomerative Clustering on Data from " + year_str)
    crash_df = gen_dataframe(year_str)

    # none_cols = find_none_vals(crash_df)
    # print("Bad columns: " + str(none_cols))

    print("Generating and Storing Cross Correlation Matrix:")
    cc_matrix = gen_cross_corr_matrix(crash_df)
    cc_matrix.to_csv("brooklyn_cc_matrix_" + year_str + ".csv")

    unimportant_cols = ["collision_id", "crash_date", "crash_time", "zip_code", "latitude", "longitude", "location",
                        "vehicle_type_code_1"]

    print("Dropping Unimportant Columns:")
    crash_df = crash_df.drop(unimportant_cols, axis=1)

    print("Performing Clustering:")
    clustered_data = agglomerative_clustering(crash_df)
    print(clustered_data)

    print("Generating Dendrogram:")
    gen_dendrogram(clustered_data, year_str)
    print("")
    return


########################################################################
agglo_functions("2019")
agglo_functions("2023")

cur.close()
conn.close()
