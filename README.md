# Recurrent Neural Network Stock Predictor

This project is a stock predictor that utilizes recurrent neural networks to predict next-day prices.

These models utilize a stock's trailing n days of data (open, high, low, close, volume) (OHLCV) to make a prediction.

![Example predictions of stocks demoing the project's trained model](https://github.com/tranjm4/stock_predictor/blob/main/predictions.png?raw=true)

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

Across all models trained, the model performed particularly well. Some particular behaviors include:

- underpredicting or overpredicting small subsections of the data
  - a special obsevation was the 30-day model underpredicting the majority of $T
- being able to follow gap-like behavior (when prices take a sharp jump)
- the 30-day model performed slightly worse than the 14-day models
  - using a Huber loss may allow for weights of insignificant n-day dependencies to collapse to zero

***

## 2. Lessons Learned

Having limited prior experience in machine learning processes (data collection/reshaping, model training), I found it a fun challenge to get involved with a complex problem such as this!

I could have pulled one of the many Kaggle datasets on historical stock data, but I wanted to familiarize myself with database design and interface design. By asking myself frequent questions about the potential design of my data, I was able to end with a design that I was happy with and that I was able to easily interface with during the model training process.

During model training, my largest roadblock was shaping the data in an appropriate format for the LSTM architecture. My PyTorch abilities were subpar starting out, but I felt I was able to better understand how to use it to my advantage to morph the data to eventually train the model.

***

## 3. Future Works

Some future tasks I have in mind include:

- incorporating additional derived features such as:
  - Exponential Moving Averages (EMA)
  - Moving Average Convergence Divergence (MACD)
- training alternative LSTM architectures (e.g., additional layers for complexity, fewer layers for compactness)
- predicting beyond next-day prices
- training a model that predicts when to buy and sell
