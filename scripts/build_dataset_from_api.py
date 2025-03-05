# scripts/build_dataset_from_api.py
import os
import time
import logging
import requests
import pandas as pd
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set up logging configuration
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def fetch_steam_apps(limit=100):
    """
    Fetch a list of apps from the Steam API and return a subset limited to 'limit' entries.
    """
    url = "https://api.steampowered.com/ISteamApps/GetAppList/v2/"
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    apps = response.json().get("applist", {}).get("apps", [])
    return apps[:limit]

def fetch_game_details(app_id):
    """
    Fetch detailed game information (price, description, genres, publisher)
    using the given App ID from the Steam store API.
    """
    try:
        url = f"https://store.steampowered.com/api/appdetails?appids={app_id}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json().get(str(app_id), {})
        if data.get("success"):
            game_data = data.get("data", {})
            title = game_data.get("name", "Unknown")
            # Convert price from cents to dollars if available
            price = game_data.get("price_overview", {}).get("final")
            price = price / 100 if price else None
            description = game_data.get("short_description", "No description available")
            genres_list = game_data.get("genres", [])
            genres = ", ".join([g["description"] for g in genres_list]) if genres_list else "Unknown"
            publishers = game_data.get("publishers", ["Unknown"])
            publisher = publishers[0] if publishers else "Unknown"
            
            return {
                "appid": app_id,
                "title": title,
                "price": price,
                "description": description,
                "genres": genres,
                "publisher": publisher
            }
    except Exception as e:
        logging.error(f"Error fetching details for app_id {app_id}: {e}")
    return None

def build_dataset_from_api(limit=100):
    """
    Builds a dataset by fetching a list of apps and retrieving detailed info for each app.
    
    Parameters:
        limit (int): Maximum number of apps to initially process.
        
    Returns:
        pandas DataFrame containing game details.
    """
    apps = fetch_steam_apps(limit)
    data = []
    for app in apps:
        app_id = app.get("appid")
        details = fetch_game_details(app_id)
        if details:
            data.append(details)
        # Pause to avoid rate limiting
        time.sleep(1)
    
    df = pd.DataFrame(data)
    return df

if __name__ == "__main__":
    # Adjust the limit as needed; for example, 300 to process more apps.
    df = build_dataset_from_api(limit=300)
    output_csv = os.path.join("data", "steam_api_data_games.csv")
    df.to_csv(output_csv, index=False)
    logging.info(f"Dataset built from API saved to: {output_csv}")
