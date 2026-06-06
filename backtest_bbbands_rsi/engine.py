import pandas as pd

CAPITAL = 100000

def backtest(df, entry_col, exit_col, capital = CAPITAL, atr_stop = 1.5, risk_pct=0.02):
    position = None
    trades = []
    equity = capital
    equity_curve = []
    current_value = 0

    for i in range(1, len(df)):
        current_row = df.iloc[i]
        prev_day = df.iloc[i - 1]

        if position == None and prev_day[entry_col] == 1:
            entry_price = (current_row['open'])
            risk_amount = equity * risk_pct          # e.g. 2% of equity = ₹2000
            stop_distance = atr_stop * current_row['atr']
            shares = risk_amount // stop_distance    # shares such that hitting stop = -2%
            
            position = {
                'entry_price': entry_price,
                'entry_date': current_row.name,
                'shares': shares,
                'stop_price': entry_price - stop_distance
            }

        elif position != None and current_row['low'] <= position['stop_price']:
            exit_price = position['stop_price']
            pnl = (exit_price - position['entry_price']) * position['shares']
            equity += pnl

            trades.append({
                'entry_date': position['entry_date'],
                'exit_date': current_row.name,
                'entry_price': position['entry_price'],
                'exit_price': exit_price,
                'pnl': pnl,
                'return_pct': (exit_price / position['entry_price'] - 1) * 100
            })

            position = None

        elif position != None and prev_day[exit_col] == 1:
            exit_price = (current_row['close'])
            pnl = (exit_price - position['entry_price']) * position['shares']
            equity += pnl

            trades.append({
                'entry_date': position['entry_date'],
                'exit_date': current_row.name,
                'entry_price': position['entry_price'],
                'exit_price': exit_price,
                'pnl': pnl,
                'return_pct': (exit_price / position['entry_price'] - 1) * 100
            })

            position = None
        
        if position is not None:
            current_value = equity - (position['entry_price'] * position['shares']) + (current_row['close'] * position['shares'])
        else:
            current_value = equity
        equity_curve.append(current_value)
        
    return trades, equity_curve
