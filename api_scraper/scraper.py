import requests
import time
import os
from pathlib import Path
import datetime
import csv
import json

import database

START_DATE = datetime.date(2022, 7, 5)
END_DATE = datetime.date(2024, 7, 5)
RATE_LIMIT = 5
CALL_INTERVAL = 60 / RATE_LIMIT
API_KEY = os.getenv("API_KEY")

BASE_URL = "https://api.polygon.io/v2/aggs"

def main():
    symbols_path = os.path.dirname(__file__) + "/request_urls.csv"
    with open(symbols_path, "r") as csvfile:
        csv_reader = csv.reader(csvfile)
        
        get_symbol_data(csv_reader)
        
        database.view_database()

def get_symbol_data(csv_reader) -> None:
    """
    Iterates through the CSV file (each symbol).
    
    For each symbol, get the API data from Polygon
    then store the data into stock_database.db (via the database.py module)
    """
    for line in csv_reader:
        symbol = line[0]
        database.insert_stock_name(symbol)
        data = fetch_data("AAPL")
        
        store_data

        time.sleep(CALL_INTERVAL + 2)
    
def fetch_data(symbol: str) -> dict | None:
    """
    Given the symbol, makes an API request to Polygon
    for the latest 2 years of daily price data.
    
    If the response is good, returns the data in JSON format.
    
    If the response is bad, returns None.
    """
    url = _get_url_from_symbol(symbol)
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None
    
def _get_url_from_symbol(symbol: str) -> str:
    """
    Creates the API request URL given the symbol.
    """
    return BASE_URL + f"/ticker/{symbol}/range/1/day/{START_DATE}/{END_DATE}"\
        + f"?adjusted=true&sort=asc&apiKey={API_KEY}"
        
def store_data(data: dict) -> None:
    save_data_csv_path = os.path.dirname(__file__) + "/saved_data.csv"
    with open(save_data_csv_path, "w") as outfile:
        json.dump(data, outfile)
    open_price = data['o']
    close_price = data['c']
    volume = data['v']
    high = data['h']
    low = data['l']
    
    

if __name__ == '__main__':
    main()