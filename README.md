# Recurrent Neural Network Stock Predictor

This project is a stock predictor that utilizes recurrent neural networks to predict next-day prices.

These models utilize a stock's trailing n days of data (open, high, low, close, volume) (OHLCV) to make a prediction.

![Example predictions of stocks demoing the project's trained model](https://github.com/tranjm4/stock_predictor/blob/main/demo.png?raw=true)

***

## 1. How It's Made

**Technologies used**: Python, PyTorch, SQLite

### 1.1 Data Collection

The data used was obtained by manually querying [Polygon's Stock API](https://polygon.io/docs/stocks) and storing that data into `api_scraper/stock_database.db`. The database design and its API is specified in `api_scraper/database.py`.

`api_scraper/scraper.py` performed this task by iterating through `api_scraper/ticker_symbols.csv`.

### 1.2 Model Training

The models were trained using LSTM (Long Short-Term Memory), which suits the sequential nature of stock data. Because the network relies on sequential data, the stock data was transformed into all possible n-day sequences for each given stock.

Among the data collected, 90% of the symbols' data (~130 symbols) were sampled to be included in training. The remaining symbols' data were reserved for post-training evaluation. This was to prevent data leakage and allow evaluations of full stock histories of a given stock.

For each stock, within each field (OHLCV), the values were scaled using min-max scaling into a (0,1) range as a way of normalizing the data across stocks.

A Mean Squared Error (MSE) loss was primarily used (a Huber loss was also used in other models), and the model was trained on this data over ~15 epochs with a batch size of 32, by which time the loss converged.

### 1.3 Model Evaluation

Given a 14-day history of a stock's OHLCV data, the model was trained to predict the 15th day's price.

Because the model was trained on values within the interval (0,1), to evaluate the model on unseen data, the outside data had to be scaled to (0,1). The model's output was compared to the scaled value of the 14th day to get a percentage change, with which we multiply to the 14th day's unscaled closing price. This gets us an unscaled predicted closing price for the 15th day using the model.

***

## 2. Lessons Learned

WORK IN PROGRESS!

### 7/20/2024

Having developed preliminary models based on solely OHLCV features, I found that it was ineffective at predicting next-day prices. Given the general trend of stocks increasing, the data was biased towards increases in prices. Therefore, the model was consistently predicting increases in next-day prices.

Moreover, it was often making conservative predictions as a result of minimizing its loss and its ability to predict strengths in next-day price movements.

Having moved towards including derived features such as EMA, MACD, and RSI, I found it an interesting challenge to make decisions on how to normalize and rescale the data. Because of the time series structure of the data, I learned that it is important to preserve local relationships while also preserving larger-scale patterns in the data.

What I am proudest of is the normalization of the MACD data. The values were often heavily skewed, but I derived a localized Z-score normalization that allowed the data to be more identically distributed :)

***

## 3. Future Works

Some future tasks I have in mind include:

- incorporating additional derived features such as:
  - Exponential Moving Averages (EMA)
  - Moving Average Convergence Divergence (MACD)
- training alternative LSTM architectures (e.g., additional layers for complexity, fewer layers for compactness)
- predicting beyond next-day prices
- training a model that predicts when to buy and sell

