import pandas as pd  # Imports Pandas Library to manipulate the data
from sqlalchemy import create_engine  # Imports the create_engine function from the SQLAlchemy library
from dotenv import load_dotenv  # Loads environment variables by importing the .env file
import os  # Imports OS to access system environment variables

load_dotenv()  # Load environment variables from .env file

# ✅ Print each environment variable to check its value
print("DB_USER:", repr(os.getenv("DB_USER")))
print("DB_PASSWORD:", repr(os.getenv("DB_PASSWORD")))
print("DB_HOST:", repr(os.getenv("DB_HOST")))
print("DB_PORT (Raw):", repr(os.getenv("DB_PORT")))  # Debugging issue
print("DB_NAME:", repr(os.getenv("DB_NAME")))

DB_USER = os.getenv("DB_USER")  # Assigns the value of the DB_USER environment variable to the DB_USER variable
DB_PASSWORD = os.getenv("DB_PASSWORD")  # Assigns the value of the DB_PASSWORD environment variable to the DB_PASSWORD variable
DB_HOST = os.getenv("DB_HOST")  # Assigns the value of the DB_HOST environment variable to the DB_HOST variable
DB_PORT = os.getenv("DB_PORT")  # Assigns the value of the DB_PORT environment variable to the DB_PORT variable
DB_NAME = os.getenv("DB_NAME")  # Assigns the value of the DB_NAME environment variable to the DB_NAME variable

#Connection to PSQL
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"  
engine = create_engine(DATABASE_URL)  # Creates a connection to the database

#Define the SQL queries
queries = {
    "Most Expensive Games": """
        SELECT title, price 
        FROM steam_games 
        ORDER BY price DESC 
        LIMIT 10;
    """,
    
    "Most Popular Genres": """
        SELECT genres, COUNT(*) AS count 
        FROM steam_games 
        GROUP BY genres 
        ORDER BY count DESC 
        LIMIT 10;
    """,
    
    "Top Rated Games": """
        SELECT title, "allReviews"
        FROM steam_games 
        WHERE "allReviews" = 'Overwhelmingly Positive' 
        LIMIT 10;
    """,
    
    "Average Price by Genre": """
        SELECT genres, ROUND(CAST(AVG(price) AS NUMERIC), 2) AS avg_price 
        FROM steam_games 
        GROUP BY genres 
        ORDER BY avg_price DESC;
    """
}

#Execute queries and print results
for query_name, query in queries.items():
    result = pd.read_sql_query(query, engine) #Runs the SQL query and stores the result in Pandas DataFrame
    print(f"\n{query_name}\n")
    print(result)