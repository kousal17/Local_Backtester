import pandas as pd
from indic_lib import *

def append_indicators(df):
    df['rsi'] = rsi(df['close'], 14)
    df['bb_mid'], df['bb_upper'], df['bb_lower'] = bollinger(df['close'], 20, 2)
    df['atr'] = atr(df, 14)
    df.dropna(inplace=True)
    return df
