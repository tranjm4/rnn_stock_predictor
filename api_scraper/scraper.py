import requests
import time
import json
import os
import csv
from pathlib import Path
import datetime

START_DATE = datetime.date(2022, 8, 1)
END_DATE = datetime.date(2024, 7, 10)

def main():
    request_urls_path = Path(os.path.dirname(__file__)) / "request_urls.csv"
    with open(request_urls_path, mode="r+") as csvfile:
        csvreader = csv.reader(csvfile, delimiter=",")
        for line in csvreader:
            print(line)

def create_stock_folder(name: str) -> None:
    """
    Creates a new folder for a stock's data within the 'data' directory
    """
    new_dir_path = Path(os.path.dirname(__file__)) / "data" / name
    os.mkdir(new_dir_path)
    


if __name__ == '__main__':
    main()
    print(START_DATE + 1)