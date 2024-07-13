import requests
import time
import os
import datetime
import csv

import database

START_DATE = datetime.date(2022,1,1)
END_DATE = datetime.date(2022,7,11)

NON_TRADING_HOLIDAYS = [
    datetime.date(2024,1,1),    # New Year's Day
    datetime.date(2023,1,2),
    datetime.date(2024,1,15),   # MLK Jr. Day
    datetime.date(2023,1,16),
    datetime.date(2022,1,17),
    datetime.date(2024,2,19),   # Washington's Bday
    datetime.date(2023,2,20),
    datetime.date(2022,2,21),
    datetime.date(2024,3,29),   # Good Friday
    datetime.date(2023,4,7),
    datetime.date(2022,4,15),
    datetime.date(2024,5,27),   # Memorial Day
    datetime.date(2023,5,29),
    datetime.date(2022,5,30),
    datetime.date(2024,6,19),   # Juneteenth Nat'l Independence Day
    datetime.date(2023,6,19),
    datetime.date(2022,6,20),
    datetime.date(2024,7,4),    # Independence Day
    datetime.date(2023,7,4),
    datetime.date(2022,7,4),
    datetime.date(2023,9,4),    # Labor Day
    datetime.date(2022,9,5),
    datetime.date(2023,11,23),  # Thanksgiving Day
    datetime.date(2022,11,24),
    datetime.date(2023,12,25),  # Christmas Day
    datetime.date(2022,12,26)
]

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
        
        data = fetch_data(symbol)
        store_data(symbol, data)

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
        
        
def store_data(symbol: str, data: dict) -> None:
    """
    Stores the API's response data into stock_database.db
    """
    results = data["results"]
    
    current_timedelta = 0
    for entry in results:
        date = START_DATE + datetime.timedelta(current_timedelta)
        
        # Adjust if holiday or weekend
        if date in NON_TRADING_HOLIDAYS:
            current_timedelta += 1
            date += datetime.timedelta(1)
        if date.weekday() == 5:
            current_timedelta += 2
            date += datetime.timedelta(2)
        elif date.weekday() == 6:
            current_timedelta += 1
            date += datetime.timedelta(1)
        # Additional check for holiday if on a monday after weekend
        if date in NON_TRADING_HOLIDAYS:
            current_timedelta += 1
            date += datetime.timedelta(1)
            
        open_price, close_price, low, high, volume = _get_stock_price_details(entry)
        current_timedelta += 1
        
        database.insert_day_prices(symbol, date,
                                   open_price, close_price,
                                   volume, low, high)
        
    
def _get_stock_price_details(entry: dict) \
    -> tuple[datetime.date, float, float, float, float, float]:
    """
    Retrieves relevant attributes from the JSON response
    (open, close, low, high, volume)
    """
    open_price = entry['o']
    close_price = entry['c']
    low = entry['l']
    high = entry['h']
    volume = entry['v']
    
    return open_price, close_price, low, high, volume


if __name__ == '__main__':
    print(API_KEY)