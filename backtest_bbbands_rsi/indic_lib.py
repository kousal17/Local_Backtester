import pandas as pd

def sma(series, window):
    return series.rolling(window).mean()

# here the series is for the data that is flowing in
# the window is the timeperiod or the number of data points to take

def ema(series, window):
    return series.ewm(span = window, adjust = False).mean()

# here there is a formula for the ema, read and understand it
# here we are just using the multiplier with the smoothing as 2 which is default.
# I could write my own loop for more control over the smoothing

# IMPORTANT: for EMA to stabilize we need to give it good number or previous inputs, to drown the noise.

def macd(series, fast = 12, slow = 26, signal = 9):
    macd_line = ema(series, fast) - ema(series, slow)
    signal_line = ema(macd_line, signal)
    histogram = macd_line - signal_line
    return macd_line, signal_line, histogram

# here the macd line is ema fast - ema slow, it is finding the momentum of the stock.
# signal is the ema of macd line
# histogram is just used as a general observation just like how we plotted the histogram for pct_changes
# the default numbers are industry standards.

def rsi(series, window = 14):
    delta = series.diff()
    gain = delta.clip(lower = 0).rolling(window).mean()
    loss = (-delta.clip(upper = 0)).rolling(window).mean()
    rs = gain / loss
    return (100 * rs) / (1 + rs)

# relative strength index is going to show us if the market is increasing/decreasing too quickly 
# 70 is good rate for increase and 30 is good rate for decreasing.

def bollinger(series, window = 20, num_devi = 2):
    middle = sma(series, window)
    std = series.rolling(window).std()
    upper = middle + (std * num_devi)
    lower = middle - (std * num_devi)
    return middle, upper, lower

# 20 is the standard number of days and here num_devi is a multipler for the std
# for num_devi = 1 we are considering 68% of the cases (on a normal distribution)
# for 2 it is 95% and 3 it is 99.7%!

def vwap(data):
    typical_price = (data['high'] + data['low'] + data['close']) / 3
    return (typical_price * data['volume']).cumsum() / data['volume'].cumsum()

# this is for intraday only!

def atr(data, window = 14):
    prev_close = data['close'].shift(1)

    distance_1 = data['high'] - data['low']
    distance_2 = (data['low'] - prev_close).abs()
    distance_3 = (data['high'] - prev_close).abs()

    true_range = pd.concat([distance_1, distance_2, distance_3], axis = 1).max(axis = 1)

    return true_range.ewm(alpha = 1/window, adjust = False).mean()

# this is used for finding volitily and mainly used for dynamic stop loss in algo trading
