import pandas as pd  #Imports Pandas Library to manipulate the data

#Load the dataset
df = pd.read_csv("data/steam_store_data_2024.csv")

#First 5 rows are displayed for quikc review
print(df.head())

#Make sure there is no missing values in the dataset
print("Missing Values:\n", df.isnull().sum())

#Displaying all column names, data types and non-null values
print("Dataset Infor:\n", df.describe())

#Basic summary of the statistics of the dataset (mean,mix,maxa and more)
print("Dataset Statistics:\n", df.describe())

