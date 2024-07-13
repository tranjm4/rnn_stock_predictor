import sqlite3
import os
import datetime
from collections import namedtuple
from pprint import pprint

import argparse

DATABASE_PATH = os.path.dirname(__file__) + "/stock_database.db"
StockData = namedtuple("Day",
                 ("date", "open_price", "close_price", "pre_market", "after_hours", "volume"))

def create_db_file():
    """
    Creates the database's .db file (only if it doesn't exist)
    """
    if not os.path.isfile(DATABASE_PATH):
        with open(DATABASE_PATH, 'a'):
            pass
    return
    

def create_database():
    try:
        connection, cursor = connect_to_db()
        
        cursor.execute("""
            PRAGMA foreign_keys = ON;               
        """)
        
        connection.commit()
        
        cursor.execute('''
            CREATE TABLE Stock (
                name VARCHAR(5) PRIMARY KEY
            );
        ''')
        connection.commit()
        cursor.execute('''
            CREATE TABLE Day (
                stockName VARCHAR(5),
                day DATE,
                open DECIMAL(6,2),
                close DECIMAL(6,2),
                low DECIMAL(6,2),
                high DECIMAL(6,2),
                volume INTEGER,
                
                PRIMARY KEY (stockName, day),
                FOREIGN KEY (stockName) REFERENCES Stock(name)
            );
        ''')
        connection.commit()
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
    finally:
        connection.close()
    
def insert_stock_name(stock_name: str) -> None:
    """
    Inserts a stock into the Stock table
    """
    try:
        connection, cursor = connect_to_db()
        
        cursor.execute(f"""INSERT INTO Stock (name) VALUES ('{stock_name}');""")
        
        connection.commit()
    except sqlite3.Error as e:
        print(f"SQLite Insert Stock error: {e}")
    finally:
        connection.close()
        
def insert_day_prices(stock_name: str, day: datetime.date,
                      open_price: float, close_price: float, volume: float,
                      low: float, high: float) -> None:
    """
    Inserts a specific company's open, close, pre-market, and after-hours, and volume
    for a specific day into the Day table
    """
    try:
        connection, cursor = connect_to_db()
        
        open_price = round(open_price, 2)
        close_price = round(close_price, 2)
        low = round(low, 2)
        high = round(high, 2)
        
        cursor.execute(f"""
            INSERT INTO Day
            (stockName, day, open, close, low, high, volume)
            VALUES ('{stock_name}', '{day}', {open_price}, {close_price}, {low}, {high}, {volume});
        """)
        connection.commit()
        print("-"*50)
        print(f"Inserted: {stock_name:<6} ({day}, {open_price:>7}, {close_price:>7}, {volume:>7}, {low:>7}, {high:>7})")
        print("-"*50)
    except sqlite3.IntegrityError as e:
        print(f"IntegrityError: {e}")
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
    finally:
        connection.close()

def view_database():
    try:
        connection, cursor = connect_to_db()
        
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print("Tables in the database:")
        for table in tables:
            print(table[0])
            
        print()
        
        cursor.execute("SELECT * FROM Stock")
        stock_table = cursor.fetchall()
        print("Stock table:")
        for stock in stock_table:
            print(stock)
        
        cursor.execute("SELECT * FROM Day")
        day_table = cursor.fetchall()
        print("Day table:")
        for day in day_table:
            print(day)
        
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
    finally:
        if connection:
            connection.close()
            
def get_stock_data(stock_name: str):
    """
    Given a stock symbol, returns the stock's historical data per day
    """
    try:
        connection, cursor = connect_to_db()
        
        cursor.execute(f"""
            SELECT day, open, close, low, high, volume
            FROM Day
            WHERE stockName = '{stock_name}'
        """)
        results = cursor.fetchall()    
        
        # Returns a StockData namedtuple with fields:
        # {date, open, close, pre_market, after_hours, volume}
        return StockData(*zip(*results))
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
    finally:
        connection.close()
        
def get_data_size():
    """
    Returns the amount of entries per stock symbol
    """
    try:
        connection, cursor = connect_to_db()
        
        cursor.execute("""
            SELECT stockName, COUNT(*)
            FROM Day
            GROUP BY stockName;
        """)
        results = cursor.fetchall()
        return results
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
    finally:
        connection.close()
        
def view_data_size():
    results = get_data_size()
    pprint(results)
    return
    
            
def clear_database():
    try:
        os.remove(DATABASE_PATH)
    except:
        pass
    create_db_file()
    create_database()
    
    print("-"*50)
    print(f"{'DATABASE CLEARED':^50}")
    print("-"*50)
    
        
def connect_to_db() -> tuple[sqlite3.Connection, sqlite3.Cursor]:
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()
    
    return connection, cursor

    
def main():
    argparser = argparse.ArgumentParser("Database.py")
    argparser.add_argument("-c", "--clear", action="store_true")
    argparser.add_argument("-p", "--print", action="store_true")
    argparser.add_argument("-l", "--length", action="store_true")
    
    args = argparser.parse_args()
    
    if args.clear:
        clear_database()
    if args.print:
        view_database()
    if args.length:
        view_data_size()
    
    
if __name__ == '__main__':
    main()