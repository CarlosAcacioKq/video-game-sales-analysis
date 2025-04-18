# Steam Game Analysis Project

## Overview
This project demonstrates how to gather, clean, and analyze Steam game data using the Steam API, Python scripts, and optional visualization tools like Tableau or Power BI. By the end of this project, you'll have a dataset of Steam games that you can explore, visualize, and expand upon for further analysis or even to build a future web application.

## Features
- **API-Based Data Collection:** Pulls game information (title, price, description, genres, publisher) directly from the Steam API.
- **Flexible Data Exploration:** Includes Python scripts for exploratory data analysis (EDA) and visualization.
- **Extensible:** Easily add more analysis steps or integrate with a web application later.

## Getting a Steam API Key
1. **Create a Steam Account:**
   - If you do not already have one, sign up at [store.steampowered.com](https://store.steampowered.com/).
2. **Visit the Steam Web API Key Page:**
   - Go to [Steam Web API Key](https://steamcommunity.com/dev/apikey) and log in with your Steam account.
3. **Register a Domain:**
   - Enter any domain name (for example, `localhost` or another placeholder) and click **Register**.
4. **Copy Your API Key:**
   - You will see a long string of characters—this is your personal Steam API key.  
   **Important:** Keep this key private and do not commit it to version control.

## Setup & Installation
1. **Clone the Repository:**
   ```bash
   git clone https://github.com/your-username/your-repo-name.git
   cd your-repo-name
   ```

2. **Create a .env File:**
   In the project's root directory, create a file named `.env` with the following content:
   ```
   STEAM_API_KEY=your_personal_steam_api_key_here
   ```
   This file is typically ignored by Git (see .gitignore).

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   It is recommended to use a virtual environment (e.g., venv or conda) to avoid conflicts with global packages.

4. **(Optional) Setup Visualization Tools:**
   If you plan to use Tableau or Power BI, install these tools separately.

## Project Structure
```
vg-sales-trends/
├── data/                  # Directory for storing CSV files
├── scripts/              # Python scripts for data collection and analysis
│   ├── build_dataset_from_api.py
│   ├── data_exploration.py
│   └── data_visualization.py
├── visuals/              # Directory for storing generated plots
├── .env                  # Environment variables (not tracked by Git)
├── .gitignore           # Git ignore file
├── README.md            # This file
└── requirements.txt     # Python package dependencies
```

## Usage
1. **Build the Dataset:**
   Run the dataset-building script:
   ```bash
   python scripts/build_dataset_from_api.py
   ```
   This will create `steam_api_data_games.csv` in the `data/` folder.

2. **Explore the Data:**
   Run the exploratory analysis script:
   ```bash
   python scripts/data_exploration.py
   ```
   This script loads the CSV and prints out descriptive statistics, value counts, and other key insights.

3. **Visualize:**
   Run the visualization script:
   ```bash
   python scripts/data_visualization.py
   ```
   Generated plots (e.g., a histogram of prices, a bar chart of the top 10 most expensive games) are saved in the `visuals/` folder.

4. **(Optional) Create Interactive Dashboards:**
   - Open Tableau or Power BI and connect to the CSV file (`data/steam_api_data_games.csv`).
   - Build interactive charts, filters, and dashboards based on your analysis.

## Visualization & Dashboards
- **Python Plots:** The generated plots are stored in the `visuals/` folder.
- **Tableau/Power BI:** Use these tools to create interactive dashboards by connecting them to the CSV file.

## Contributing
1. Fork this repository.
2. Create a new branch for your feature or bug fix.
3. Commit and push your changes.
4. Submit a Pull Request describing your modifications.

## License
This project is provided for educational purposes. Please respect the Steam API Terms of Use when making requests. You are free to modify and distribute this code, but the authors disclaim any liability for its usage.
