from loader import load
from indicators import append_indicators
from engine import backtest
from report import report

def run():
    ticker = "INDIGO"
    df = load(ticker)
    print(ticker + "Strat = BB Bands + RSI")

    df = append_indicators(df)

    split = int(len(df) * 0.7)
    train = df.iloc[:split].copy()
    test = df.iloc[split:].copy()

    train['entry_signal'] = (train['rsi'] < 35) & (train['close'] <= train['bb_lower'] * 1.01)
    train['exit_signal'] = (train['close'] >= train['bb_mid']) | (train['rsi'] > 65)

    test['entry_signal'] = (test['rsi'] < 35) & (test['close'] <= test['bb_lower'] * 1.01)
    test['exit_signal'] = (test['close'] >= test['bb_mid']) | (test['rsi'] > 65)

    train_trades, train_eq = backtest(train, 'entry_signal', 'exit_signal')
    test_trades, test_eq = backtest(test, 'entry_signal', 'exit_signal')

    print("     TRAIN")
    report(train_trades, train_eq)
    print("     TEST")
    report(test_trades, test_eq)

run()
