# scripts/data_exploration.py
import pandas as pd
import os

def explore_data(csv_path):
    """
    Loads the API-sourced CSV and prints basic EDA findings.
    """
    # Load the dataset from the given CSV path
    df = pd.read_csv(csv_path)
    
    # Print the shape of the dataset (number of rows and columns)
    print(f"Dataset shape: {df.shape}\n")
    
    # Show column names, non-null counts, and dtypes
    print("Columns and Data Types:")
    print(df.info(), "\n")
    
    # Display basic descriptive statistics for numeric columns
    print("Basic Descriptive Statistics (Numeric):")
    print(df.describe(), "\n")
    
    # Display descriptive statistics for categorical data
    print("Descriptive Statistics (Categorical):")
    print(df.describe(include='object'), "\n")
    
    # Example: Count of genres (if available)
    if 'genres' in df.columns:
        print("Top 5 most common genres:")
        print(df['genres'].value_counts().head(), "\n")
    
    # Example: Price distribution details
    if 'price' in df.columns:
        print("Price Distribution:")
        print(df['price'].describe(), "\n")
    
    # Example: Listing first few game titles to verify data
    if 'title' in df.columns:
        print("Sample Game Titles:")
        print(df['title'].head(10), "\n")

if __name__ == "__main__":
    # Use the new CSV built from the API data
    csv_path = os.path.join("data", "steam_api_data_games.csv")
    explore_data(csv_path)
