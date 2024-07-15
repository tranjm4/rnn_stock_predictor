# Recurrent Neural Network Stock Predictor

This project is a stock predictor that utilizes recurrent neural networks to predict next-day prices.

These models utilize a stock's trailing n days of data (open, high, low, close, volume) (OHLCV) to make a prediction.

![Example predictions of stocks demoing the project's trained model](https://github.com/tranjm4/stock_predictor/blob/main/predictions.png?raw=true)

***

## 1. How It's Made

**Technologies used**: Python, PyTorch, SQLite

### 1.1 Data Collection

The data used was obtained by manually querying [Polygon's Stock API](https://polygon.io/docs/stocks) and storing that data into `api_scraper/stock_database.db`. The database design is specified in `api_scraper/database.py`.

`api_scraper/scraper.py` performed this task by iterating through `api_scraper/ticker_symbols.csv`.

### 1.2 Model Training

The 