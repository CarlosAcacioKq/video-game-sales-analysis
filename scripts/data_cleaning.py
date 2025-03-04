import pandas as pd  # Imports Pandas Library to manipulate the data
import requests  # Imports Requests Library to fetch data from APIs
import time  # Imports Time Library to manage request delays
from dotenv import load_dotenv  # Loads environment variables by importing the .env file
import os  # Imports OS to access system environment variables
from sqlalchemy import create_engine  # Imports SQLAlchemy for database connection

# ✅ Load environment variables from .env file
load_dotenv()

# ✅ Fetch database credentials from .env file
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME")

# ✅ Create PostgreSQL connection
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URL)

# ✅ Fetch Steam API Key from .env file
STEAM_API_KEY = os.getenv("STEAM_API_KEY")

# ✅ Load the dataset
df = pd.read_csv("data/steam_store_data_2024.csv")

""" ALL OF THE FOLLOWING LINES WILL LOOK TO HANDLE MISSING VALUES BY CONNECTING TO THE STEAM API AND FETCHING INFORMATION
IF THE MISSING INFORMATION IS NOT AVAILABLE IN THE API, IT WILL BE FILLED WITH A DEFAULT VALUE """

def get_steam_data(game_title):
    """ Fetches missing game details (price, description, genre, publisher) from Steam API using the game title """

    try:
        # Search for the game App ID using the Steam API
        search_url = f"https://api.steampowered.com/ISteamApps/GetAppList/v2/"
        response = requests.get(search_url, timeout=10)  # Limits request time to 10 seconds
        
        # Extracts the full list of Steam games
        app_list = response.json().get("applist", {}).get("apps", [])

        # Before doing anything, checks if the list is empty
        if not app_list:
            return None, None, None, None  # No game data found

        # Finds the App ID for the requested video game
        matching_games = [game for game in app_list if game_title.lower() in game["name"].lower()]
        if not matching_games:
            return None, None, None, None  # No match found

        app_id = matching_games[0]["appid"]  # Selects the first matching App ID
        
        # Uses the App ID to fetch the game's details
        game_url = f"https://store.steampowered.com/api/appdetails?appids={app_id}"
        game_response = requests.get(game_url, timeout=10)  # Limits request time to 10 seconds

        # Raises an HTTP error if the request fails
        game_response.raise_for_status()

        game_data = game_response.json()

        # Ensures that the API response has usable data
        if not game_data:
            return None, None, None, None  # No valid game data received
        
        # Retrieves game data if available
        game_info = game_data.get(str(app_id), {}).get("data", {})

        # Extracts the price details
        price = game_info.get("price_overview", {}).get("final", None)
        if price is not None:
            price = price / 100  # Converts the price from cents to dollars

        # Extracts other game details
        description = game_info.get("short_description", "No description available")
        genres = ", ".join([genre["description"] for genre in game_info.get("genres", [])]) if "genres" in game_info else "Unknown"
        publisher = game_info.get("publishers", ["Unknown"])[0] if "publishers" in game_info else "Unknown"

        return price, description, genres, publisher  # Returns fetched data

    except requests.exceptions.HTTPError as http_err:
        # Raised when an HTTP error occurs (e.g., 404 Not Found, 500 Server Error)
        print(f"❌ HTTP error occurred for {game_title}: {http_err}")

    except requests.exceptions.ConnectionError:
        # Raised when there is a network issue (e.g., no internet, server is down)
        print(f"❌ Connection error: Unable to reach Steam API for {game_title}.")

    except requests.exceptions.Timeout:
        # Raised when the request takes longer than the specified timeout
        print(f"⏳ Timeout error: Steam API took too long to respond for {game_title}.")

    except requests.exceptions.RequestException as req_err:
        # A generic exception for all other request-related errors
        print(f"❌ Unexpected error occurred for {game_title}: {req_err}")

    except KeyError as key_err:
        # Raised when the API response is missing an expected field (e.g., "data" or "price_overview")
        print(f"❌ Key error: Missing expected field in API response for {game_title}. {key_err}")

    except Exception as e:
        # A general catch-all exception to prevent unexpected crashes
        print(f"⚠️ General error fetching Steam data for {game_title}: {e}")

    return None, None, None, None  # Returns None if an error occurs   

# ✅ Removes the "$" symbol from the price column if present
df['price'] = df['price'].astype(str).str.replace('$', '', regex=True)

# ✅ Converts "price" column to numeric (handling missing values)
df['price'] = pd.to_numeric(df['price'], errors='coerce')

# ✅ Iterates through the dataset to fetch missing values
for index, row in df.iterrows():
    # Checks if price or description is missing for a game
    if pd.isnull(row['price']) or pd.isnull(row['description']):
        # Calls Steam API to fetch missing details
        steam_price, steam_description, steam_genres, steam_publisher = get_steam_data(row['title'])

        # Updates price if found
        if steam_price is not None:
            df.at[index, 'price'] = steam_price

        # Updates description if found
        if steam_description is not None:
            df.at[index, 'description'] = steam_description

        # Updates genres if found
        if steam_genres is not None:
            df.at[index, 'genres'] = steam_genres

        # Updates publisher if found
        if steam_publisher is not None:
            df.at[index, 'publisher'] = steam_publisher

    # Pauses for 1 second to prevent Steam API rate limiting
    time.sleep(1)

# ✅ Fills any remaining missing values with default values
df['price'].fillna(df['price'].median(), inplace=True)  # Replaces missing prices with the median price
df['description'].fillna("No description available", inplace=True)  # Replaces missing descriptions
df['genres'].fillna("Unknown", inplace=True)  # Replaces missing genres with "Unknown"
df['publisher'].fillna("Unknown", inplace=True)  # Replaces missing publishers with "Unknown"

# ✅ Saves the cleaned dataset to a new file
df.to_csv("data/cleaned_steam_store_data_2024.csv", index=False)
print("✅ Cleaned data saved to 'cleaned_steam_store_data_2024.csv'")

# ✅ Insert cleaned data into PostgreSQL
df.to_sql("steam_games", engine, if_exists="replace", index=False)
print(f"✅ {len(df)} rows inserted into PostgreSQL database!")
