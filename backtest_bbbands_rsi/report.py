import pandas as pd
from loader import calc_years_diff
from engine import CAPITAL
from math import sqrt

def report(trades, equity_curve, capital = CAPITAL):
    if not trades:
        print("There are no trades executed")
        return
    
    df = pd.DataFrame(trades)
    wins = df[df['pnl'] > 0]

    total_return = (equity_curve[-1] - capital) / capital * 100
    win_rate = len(wins) / len(df) * 100
    avg_win = wins['pnl'].mean() if len(wins) else 0
    avg_loss = df[df['pnl'] <= 0]['pnl'].mean() if len(df[df['pnl'] <= 0]) else 0

    years = calc_years_diff()
    cagr = (((1 + (total_return / 100)) ** (1 / years)) - 1) * 100

    eq = pd.Series(equity_curve)
    rolling_max = eq.cummax()
    drawdown = (eq - rolling_max) / rolling_max
    max_dd = drawdown.min() * 100

    # daily_returns = eq.diff() / eq.shift(1)
    daily_returns = eq.pct_change()
    sharpe_ratio = (daily_returns.mean() / daily_returns.std()) * sqrt(252)


    print(f"Trades:        {len(df)}")
    print(f"Win Rate:      {win_rate:.1f}%")
    print(f"Abs. Returns:  {total_return:.2f}%")
    print(f"CAGR:          {cagr:.3f}%")
    print(f"Max Drawdown:  {max_dd:.2f}%")
    print(f"Avg Win:       {avg_win:.0f}")
    print(f"Avg Loss:      {avg_loss:.0f}")
    print(f"Expectancy:    {df['pnl'].mean():.0f} per trade")
    print(f"Sharpe Ratio:  {sharpe_ratio:.3f}")
