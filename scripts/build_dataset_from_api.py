# scripts/build_dataset_from_api.py
import os
import time
import logging
import requests
import pandas as pd
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from dotenv import load_dotenv
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from collections import Counter

# Load environment variables from .env file
load_dotenv()

# Set up logging configuration
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Configuration
MIN_REVIEWS = 10  # Reduced minimum number of reviews
MIN_METACRITIC = 0  # Removed minimum metacritic score requirement
MAX_PRICE = 100  # Maximum price in dollars
MIN_RELEASE_DATE = "2010-01-01"  # Extended minimum release date to get more games
MAX_WORKERS = 1  # Single worker to avoid rate limiting
REQUEST_DELAY = 2  # Delay between requests in seconds
MAX_RETRIES = 3  # Maximum number of retries for failed requests
TEST_LIMIT = 1000  # Increased limit to process more games

# Set up requests session with retry strategy
session = requests.Session()
retry_strategy = Retry(
    total=MAX_RETRIES,
    backoff_factor=1,
    status_forcelist=[429, 500, 502, 503, 504],
)
adapter = HTTPAdapter(max_retries=retry_strategy)
session.mount("http://", adapter)
session.mount("https://", adapter)

# Add headers to mimic a browser
session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'application/json',
    'Accept-Language': 'en-US,en;q=0.9',
    'Connection': 'keep-alive',
})

def get_game_details(app_id):
    """Get detailed information for a game."""
    try:
        # Get detailed game info
        details_url = f"https://store.steampowered.com/api/appdetails?appids={app_id}"
        details_response = session.get(details_url)
        details_response.raise_for_status()
        details_data = details_response.json()
        
        if not details_data or str(app_id) not in details_data:
            return None
            
        game_data = details_data[str(app_id)]
        if not game_data.get('success'):
            return None
            
        data = game_data.get('data', {})
        
        # Get price info
        price_info = data.get('price_overview', {})
        price = price_info.get('final_formatted', 'N/A')
        if price != 'N/A':
            try:
                price = float(price.replace('$', '').replace(',', '').replace('₩', '').strip())
            except ValueError:
                price = 'N/A'
        
        # Get release date
        release_date = data.get('release_date', {}).get('date', 'N/A')
        if release_date != 'N/A':
            try:
                release_date = datetime.strptime(release_date, '%d %b, %Y').strftime('%Y-%m-%d')
            except ValueError:
                release_date = 'N/A'
        
        # Get categories and genres
        categories = [cat.get('description', '') for cat in data.get('categories', [])]
        genres = [genre.get('description', '') for genre in data.get('genres', [])]
        
        # Get platforms
        platforms = data.get('platforms', {})
        windows = platforms.get('windows', False)
        mac = platforms.get('mac', False)
        linux = platforms.get('linux', False)
        
        # Get achievements and DLC info
        has_achievements = any(cat == 'Steam Achievements' for cat in categories)
        has_dlc = bool(data.get('dlc', []))
        
        # Get review info
        review_score = data.get('metacritic', {}).get('score', 'N/A')
        review_count = data.get('recommendations', {}).get('total', 0)
        
        # Get developer and publisher
        developers = data.get('developers', ['N/A'])
        publishers = data.get('publishers', ['N/A'])
        
        return {
            'app_id': app_id,
            'name': data.get('name', 'N/A'),
            'price': price,
            'release_date': release_date,
            'categories': categories,
            'genres': genres,
            'windows': windows,
            'mac': mac,
            'linux': linux,
            'has_achievements': has_achievements,
            'has_dlc': has_dlc,
            'review_score': review_score,
            'review_count': review_count,
            'developer': developers[0] if developers else 'N/A',
            'publisher': publishers[0] if publishers else 'N/A',
            'description': data.get('short_description', 'N/A'),
            'website': data.get('website', 'N/A'),
            'support_url': data.get('support_info', {}).get('url', 'N/A'),
            'header_image': data.get('header_image', 'N/A'),
            'background_image': data.get('background', 'N/A'),
            'screenshots': [screenshot.get('path_full', '') for screenshot in data.get('screenshots', [])],
            'movies': [movie.get('webm', {}).get('480', '') for movie in data.get('movies', [])],
            'tags': [tag.get('name', '') for tag in data.get('tags', [])]
        }
    except Exception as e:
        logging.error(f"Error getting details for app {app_id}: {str(e)}")
        return None

def get_featured_games():
    """Get featured games from Steam store."""
    try:
        # Get featured games from Steam store
        store_url = "https://store.steampowered.com/api/featuredcategories"
        response = session.get(store_url)
        response.raise_for_status()
        data = response.json()
        
        # Get games from various categories
        games = []
        
        # Featured games
        if 'featured_win' in data:
            games.extend(data['featured_win'].get('items', []))
        
        # Specials (discounted games)
        if 'specials' in data:
            games.extend(data['specials'].get('items', []))
        
        # New releases
        if 'new_releases' in data:
            games.extend(data['new_releases'].get('items', []))
        
        # Top sellers
        if 'top_sellers' in data:
            games.extend(data['top_sellers'].get('items', []))
        
        # Coming soon
        if 'coming_soon' in data:
            games.extend(data['coming_soon'].get('items', []))
        
        # Remove duplicates based on app_id
        unique_games = {game['id']: game for game in games}.values()
        
        logging.info(f"Successfully fetched {len(unique_games)} games from Steam")
        return list(unique_games)
    except Exception as e:
        logging.error(f"Error fetching featured games: {str(e)}")
        return []

def process_game(game):
    """Process a single game and return its details if it meets criteria."""
    try:
        app_id = game['id']
        details = get_game_details(app_id)
        
        if not details:
            return None
            
        # Only filter out games with invalid prices (keep games with N/A prices)
        if details['price'] != 'N/A' and details['price'] > MAX_PRICE:
            return None
            
        # Remove release date filter to include more games
        # if details['release_date'] != 'N/A' and details['release_date'] < MIN_RELEASE_DATE:
        #     return None
            
        # Remove review count filter to include more games
        # if details['review_count'] < MIN_REVIEWS:
        #     return None
            
        return details
    except Exception as e:
        logging.error(f"Error processing game {game.get('name', 'Unknown')}: {str(e)}")
        return None

def main():
    """Main function to build dataset from Steam API."""
    try:
        # Get featured games
        games = get_featured_games()
        if not games:
            logging.error("No games found")
            return
            
        # Process games
        processed_games = []
        successful_count = 0
        
        for i, game in enumerate(games[:TEST_LIMIT], 1):
            logging.info(f"Processing game {i}/{TEST_LIMIT}: {game.get('name', 'Unknown')}")
            
            details = process_game(game)
            if details:
                processed_games.append(details)
                successful_count += 1
                logging.info(f"Successfully processed game: {details['name']}")
            
            # Log progress every 5 games
            if i % 5 == 0:
                logging.info(f"Processed {i}/{TEST_LIMIT} games (Successful: {successful_count})")
            
            # Add delay between requests
            time.sleep(REQUEST_DELAY)
        
        if not processed_games:
            logging.error("No games met the criteria")
            return
            
        # Convert to DataFrame
        df = pd.DataFrame(processed_games)
        
        # Save to CSV with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"data/steam_popular_games_{timestamp}.csv"
        df.to_csv(output_file, index=False)
        logging.info(f"Dataset built from API saved to: {output_file}")
        
        # Log statistics
        logging.info(f"Total games processed: {len(processed_games)}")
        
        # Calculate average price for non-N/A prices
        numeric_prices = [p for p in df['price'] if isinstance(p, (int, float))]
        if numeric_prices:
            avg_price = sum(numeric_prices) / len(numeric_prices)
            logging.info(f"Average price: ${avg_price:.2f}")
        else:
            logging.info("No valid prices found to calculate average")
        
        # Get most common genres
        all_genres = [genre for genres in df['genres'] for genre in genres]
        genre_counts = Counter(all_genres)
        logging.info(f"Most common genres: {dict(genre_counts.most_common(5))}")
        
        # Get top 10 games by review count
        logging.info("\nTop 10 games by review count:")
        top_games = df.nlargest(10, 'review_count')
        for _, game in top_games.iterrows():
            price_str = f"${game['price']}" if isinstance(game['price'], (int, float)) else str(game['price'])
            logging.info(f"{game['name']}: {game['review_count']} reviews, {price_str}, Metacritic: {game['review_score']}")
        
        # Additional statistics
        logging.info("\nAdditional Statistics:")
        logging.info(f"Games with achievements: {df['has_achievements'].sum()}")
        logging.info(f"Games with DLC: {df['has_dlc'].sum()}")
        logging.info(f"Windows supported: {df['windows'].sum()}")
        logging.info(f"Mac supported: {df['mac'].sum()}")
        logging.info(f"Linux supported: {df['linux'].sum()}")
        
    except Exception as e:
        logging.error(f"Error in main function: {str(e)}")
        raise

if __name__ == "__main__":
    main()
