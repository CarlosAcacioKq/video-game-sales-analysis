Features
• API-Based Data Collection: Pulls game information (title, price, description, genres, publisher) directly from the Steam API.
• Limit Parameter: Adjust the number of apps fetched from Steam (e.g., 100, 300, etc.).
• Flexible Data Exploration: Includes Python scripts for exploratory data analysis (EDA) and visualization.
• Easily Extensible: Expandable for additional analysis, dashboards, or integration with a web application.

Getting a Steam API Key

Create a Steam Account:
If you do not already have one, sign up at store.steampowered.com.
Visit the Steam Web API Key Page:
Go to https://steamcommunity.com/dev/apikey and log in with your Steam account.
Register a Domain:
Enter any domain name (for example, "localhost" or another placeholder) and click “Register.”
Copy Your API Key:
You will see a long string of characters; this is your personal Steam API key.
Important: Keep this key private and do not commit it to version control.
Setup & Installation

Clone the Repository:
Open your terminal and run:
git clone https://github.com/your-username/your-repo-name.git
Navigate to the project folder:
cd your-repo-name
Create a .env File:
In the root directory of the project, create a file named .env with the following content:
STEAM_API_KEY=your_personal_steam_api_key_here
(Note: This file is typically ignored by Git to keep your key secure.)
Install Dependencies:
Run:
pip install -r requirements.txt
It is recommended to use a virtual environment (e.g., venv or conda) to avoid conflicts with global packages.
(Optional) Setup Visualization Tools:
If you plan to use Tableau or Power BI, install these tools separately. They are not installed via pip.
Project Structure
• data/
  - Contains CSV files, including the generated steam_api_data_games.csv from the API.
• scripts/
  - build_dataset_from_api.py: Script to fetch game data from the Steam API.
  - data_exploration.py: Script for performing exploratory data analysis (EDA).
  - data_visualization.py: Script for creating plots (e.g., price distribution, top 10 most expensive games).
• visuals/
  - Contains generated image files (e.g., .png files for plots).
• dashboards/
  - (Optional) Contains Tableau or Power BI dashboard files.
• .env
  - Stores your STEAM_API_KEY and other sensitive variables.
• requirements.txt
  - Lists Python dependencies.
• README.md
  - This document, providing an overview and instructions for the project.

Usage

Building the Dataset

Run the dataset-building script:
  python scripts/build_dataset_from_api.py
  - This will create the file steam_api_data_games.csv in the data folder.
Data Exploration
2. Run the exploratory analysis script:
  python scripts/data_exploration.py
  - This script loads the CSV and prints descriptive statistics, value counts, and other key insights to the console.

Visualization
3. Run the visualization script:
  python scripts/data_visualization.py
  - The script generates plots (for example, a histogram of prices and a bar chart of the top 10 most expensive games) and saves them to the visuals folder.

Optional Dashboard Creation
4. If you wish to create interactive dashboards:
  - Open Tableau or Power BI and connect to the CSV file (steam_api_data_games.csv).
  - Build interactive charts, filters, and dashboards based on your analysis.

Visualization & Dashboards

Python Plots: The generated plots are stored in the visuals/ folder.
Tableau / Power BI: Use these tools to create interactive dashboards by connecting them to the CSV file.
Contributing
• Fork this repository.
• Create a new branch for your feature or bug fix.
• Commit and push your changes.
• Submit a Pull Request describing your changes.

License
This project is provided for educational purposes. You’re free to modify and distribute this code, but please respect the Steam API Terms of Use when making requests. The author(s) disclaim any liability for usage.

Enjoy exploring Steam game data! If you have any questions or run into issues, please open an issue or contact the project maintainers.
