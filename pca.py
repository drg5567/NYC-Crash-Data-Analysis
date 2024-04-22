import pymysql
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

"""
Perform principal components analysis on a dataset of Brooklyn traffic incidents for June 2020 and June 2022

@author: Danny Gardner      drg5567
"""


conn = pymysql.connect(host='localhost', user='root', password='w00dlandAllianc3', db="brooklyn_crashes")
cur = conn.cursor()

np.set_printoptions(suppress=True)


def format_date(date):
    return date.strftime('%Y-%m-%d')


def gen_dataframe(year_str, month_str, day_str):
    """
    Gather data from the database and generate the dataframe to be used
    :param year_str: the given year
    :param month_str: the given month
    :param day_str: the last day of the given month
    :return: the dataframe
    """
    sql_stmt = ("SELECT * FROM crash_data "
                "WHERE crash_date BETWEEN "
                "'" + year_str + "-" + month_str + "-01' AND '" + year_str + "-" + month_str + "-" + day_str + "' ")
    cur.execute(sql_stmt)
    results = cur.fetchall()
    columns = [desc[0] for desc in cur.description]

    df = pd.DataFrame(results, columns=columns)

    # Clean the numeric data by rounding values and removing nulls
    df["zip_code"] = df["zip_code"].fillna(0)
    df["latitude"] = df["latitude"].fillna(0)
    df["longitude"] = df["longitude"].fillna(0)

    df["latitude"] = df["latitude"].round(3)
    df["longitude"] = df["longitude"].round(3)

    df["crash_date"] = df["crash_date"].apply(format_date)
    df["crash_time"] = df["crash_time"].astype(str).str[7:]

    # Encode the string columns
    string_cols = ["crash_date", "crash_time", "location", "on_street_name", "cross_street_name", "off_street_name",
                   "contributing_factor_vehicle_1", "contributing_factor_vehicle_2", "contributing_factor_vehicle_3",
                   "contributing_factor_vehicle_4", "contributing_factor_vehicle_5", "vehicle_type_code_1",
                   "vehicle_type_code_2", "vehicle_type_code_3", "vehicle_type_code_4", "vehicle_type_code_5"]

    for col in string_cols:
        df[col] = df[col].astype('category').cat.codes

    return df


def clean_eigens(dataframe, eigenvals):
    """
    Sort and normalize the collection of eigenvalues
    :param dataframe: the dataframe containing the eigenvalues and their respective eigenvectors
    :param eigenvals: the list of eigenvalues
    :return: the list of normalized eigenvalues along with the sorted dataframe
    """
    sorted_eigenvals = -np.sort(-eigenvals)

    sorted_df = pd.DataFrame(columns=dataframe.columns)
    for i in range(len(dataframe)):
        val = sorted_eigenvals[i]
        vector = dataframe[dataframe["Eigenvalue"] == val].values[0][2]
        sorted_row = {"ID": i, "Eigenvalue": val, "Eigenvector": vector}
        sorted_df.loc[i] = sorted_row

    total = np.sum(sorted_eigenvals)
    normalized_eigenvals = sorted_eigenvals/total
    return normalized_eigenvals, sorted_df


def plot_eigenval_sum(eigenvals, month, year):
    """
    Plot the eigenvalue sum for a given set of eigenvalues for a year and month
    :param eigenvals: the list of eigenvalues
    :param month: the month of the data
    :param year: the year of the data
    :return: None
    """
    x = []
    y = []
    cum_sum = 0
    for i in range(len(eigenvals) + 1):
        x.append(i)
        y.append(cum_sum)
        if i == len(eigenvals):
            break
        cum_sum += eigenvals[i]

    plt.figure()
    plt.plot(x, y, marker='o', color='blue')
    plt.xlabel("Number of Eigenvalues")
    plt.ylabel("Cumulative Sum")
    plt.title("Cumulative Sum of Eigenvalues")
    plt.savefig("sum_of_eigenvalues_" + month + "_" + year + ".png")
    return


def project_data(data, eigenvects, filename, month, year):
    """
    Project a given dataset onto a collection of eigenvectors. The projected data is then plotted as a scatterplot
    and stored.
    :param data: the dataset
    :param eigenvects: the important eigenvectors
    :param filename: the filename to save the plot as
    :return: the projected data
    """
    projected_data = np.dot(data, eigenvects.T)

    plt.figure(figsize=(10, 5))
    project_df = pd.DataFrame(projected_data, columns=["PC" + str(i) for i in range(1, len(eigenvects) + 1)])
    plt.scatter(project_df["PC1"], project_df["PC2"])
    plt.xlabel("Principal Component 1")
    plt.ylabel("Principal Component 2")
    plt.title("Brooklyn Crash Data from " + month + "/" + year + " Projected onto First 2 Eigenvectors")
    plt.savefig(filename)
    return projected_data


def k_means(dataframe, k):
    """
    Calculates the k-means algorithm on the dataset to use for comparison
    :param dataframe: the dataset
    :param k: the number of clusters to make
    :return: None
    """

    k_means_cluster = KMeans(n_clusters=k)
    k_means_cluster.fit(dataframe)
    cents = k_means_cluster.cluster_centers_
    print("K-Means Centroids: ")
    print(cents)
    return cents


def elbow_kmeans(dataframe, month, year):
    """
    Generate an elbow graph for k-means clustering
    :param dataframe: the given dataframe
    :param month: the month of the data
    :param year: the year of the data
    :return: None
    """
    inertias = []
    for i in range(1, 11):
        k_means_cluster = KMeans(n_clusters=i)
        k_means_cluster.fit(dataframe)
        inertias.append(k_means_cluster.inertia_)

    plt.figure()
    plt.plot(range(1, 11), inertias, marker='o')
    plt.title('Elbow method')
    plt.xlabel('Number of clusters')
    plt.ylabel('Inertia')
    plt.savefig("kmeans_elbow_graph_" + month + "_" + year + ".png")
    return


def pca(year, month, day, num_centroids):
    """
    Perform principal components analysis on the car accidents for the given time period
    :param year: the given year
    :param month: the given month
    :param day: the last day of the month
    :param num_centroids: the number of centroids to use
    :return: None
    """
    print("Performing PCA on crash data from " + month + "/" + year)
    crash_df = gen_dataframe(year, month, day)
    crash_df = crash_df.drop(columns=["collision_id"])

    covar_matrix = crash_df.cov()

    # Generate and round the eigenvalues and eigenvectors
    eigenvalues, eigenvectors = np.linalg.eig(covar_matrix)
    eigenvalues = np.round(eigenvalues, decimals=2)
    eigenvectors = np.round(eigenvectors, decimals=2)

    # Create a dataframe to keep track of the eigenvalue and eigenvector pairs
    eigen_df = pd.DataFrame(columns=["ID", "Eigenvalue", "Eigenvector"])
    for i in range(len(eigenvalues)):
        value = eigenvalues[i]
        vector = eigenvectors[i]
        eigen_df.loc[i] = {"ID": i, "Eigenvalue": value, "Eigenvector": vector}

    # Sort and normalize the eigenvalues to use for the sum plot
    normalized_eigenvalues, eigen_df = clean_eigens(eigen_df, eigenvalues)
    plot_eigenval_sum(normalized_eigenvalues, month, year)

    print("First 3 EigenVectors")
    first_three = np.empty((3, 27))
    for i in range(0, 3):
        vec = eigen_df.at[i, "Eigenvector"]
        print(vec)
        first_three[i] = vec

    # Project the data to use for k-means clustering
    projected_shopping_data = project_data(crash_df, first_three[:2],
                                           "brooklyn_projection_" + month + "_" + year + ".png", month, year)
    elbow_kmeans(projected_shopping_data, month, year)
    centroids = k_means(projected_shopping_data, num_centroids)

    print("\nCentroids Re-Projected onto First 2 Eigenvectors")
    reverted_centroids = np.dot(centroids, first_three[:2])
    reverted_centroids = np.round(reverted_centroids, decimals=2)
    print(reverted_centroids)
    print("")
    return


###################################################################################################
pca("2020", "06", "30", 4)
pca("2022", "06", "30", 3)
