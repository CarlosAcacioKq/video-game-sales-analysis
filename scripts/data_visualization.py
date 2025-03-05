# scripts/data_visualization.py
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def create_visuals(csv_path, visuals_dir):
    """
    Creates and saves basic data visualizations from the API-sourced CSV.
    Visualizations include:
    - Price distribution histogram
    - Bar chart for top 10 most expensive games
    - Bar chart for most common genres
    """
    # Load the CSV into a DataFrame
    df = pd.read_csv(csv_path)
    
    # Replace infinite values with NaN to avoid warnings
    df.replace([np.inf, -np.inf], np.nan, inplace=True)
    
    # Ensure the visuals folder exists
    if not os.path.exists(visuals_dir):
        os.makedirs(visuals_dir)
    
    # Visual 1: Distribution of Prices
    if 'price' in df.columns:
        plt.figure(figsize=(8, 6))
        sns.histplot(df['price'], bins=20, kde=True)
        plt.title("Price Distribution")
        plt.xlabel("Price ($)")
        plt.ylabel("Frequency")
        plt.tight_layout()
        plt.savefig(os.path.join(visuals_dir, "price_distribution.png"))
        plt.close()
    
    # Visual 2: Top 10 Most Expensive Games
    if 'price' in df.columns and 'title' in df.columns:
        top_expensive = df.nlargest(10, 'price')
        plt.figure(figsize=(10, 6))
        sns.barplot(data=top_expensive, x='price', y='title', palette='viridis')
        plt.title("Top 10 Most Expensive Games")
        plt.xlabel("Price ($)")
        plt.ylabel("Game Title")
        plt.tight_layout()
        plt.savefig(os.path.join(visuals_dir, "top_10_most_expensive_games.png"))
        plt.close()
    
    # Visual 3: Most Common Genres
    if 'genres' in df.columns:
        # Split comma-separated genres into individual genre items
        genre_series = df['genres'].dropna().apply(lambda x: [genre.strip() for genre in x.split(",")])
        # Flatten the list and count each genre occurrence
        genre_counts = pd.Series([genre for sublist in genre_series for genre in sublist]).value_counts()
        plt.figure(figsize=(10, 6))
        sns.barplot(x=genre_counts.values, y=genre_counts.index, palette='coolwarm')
        plt.title("Most Common Genres")
        plt.xlabel("Count")
        plt.ylabel("Genre")
        plt.tight_layout()
        plt.savefig(os.path.join(visuals_dir, "most_common_genres.png"))
        plt.close()

if __name__ == "__main__":
    csv_path = os.path.join("data", "steam_api_data_games.csv")
    visuals_dir = "visuals"
    create_visuals(csv_path, visuals_dir)
