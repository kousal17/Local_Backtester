# Local_Backtester
An end-to-end local data pipeline and backtesting engine built from scratch in Python. This project serves as a foundational infrastructure workspace designed to tackle the two most critical pillars of quantitative strategy development: High-Fidelity Data Architecture and Deterministic Backtesting..


## 🛠️ System Architecture & Features
The repository is split into two primary components: an incremental data ingestion pipeline and an event-driven feature/backtesting matrix.

### 1. Dual-Exchange Data
Both the National Stock Exchange (NSE) and the Bombay Stock Exchange (BSE) using ticker verification and tracking systems.

Multi-Timeframe Storage Grid: Downloads, formats, and stores data rows across different time intervals: 1m, 2m, 5m, 1h, and 1d intervals.

Incremental Appending (Delta Loading): To maximize network efficiency and minimize API calls, the script parses existing local CSV files, identifies the last recorded historical timestamp, and appends only fresh market candles.

### 2. Backtesting & Feature Engineering Workspace
Vectorized Feature Mapping: A list of indicators in (indic_lib.py) can be appended to the pandas data frame using the pre-built vectorized form that pandas uses, directly to the dataframe that will be used for further computation.

Signal Generation Engine: Rule-based logic to trigger execution entry and exit streams based on custom mathematical conditions,that use the indicators, provided.

## 🚀 Getting Started
Prerequisites
Make sure you have Python 3.10+ installed along with the required libraries:

pandas, yfinance, pytz

Bash
pip install pandas yfinance pytz

## Quick Usage Example
Store both the folders in one folder and you are good to go.

### Storing and Collecting Data:
Start off by loading tickers into ticker_list.csv, for example "RELIANCE", in the default format.
Then run update.py, to store csv data for the tickers. (the ticker will then be stored in saved_ticker.csv)

For updating previously stored data, run update.py after 4 PM (IST) and the code will automatically update all the csvs that were previously loaded (the run_log.csv will save all the save update runs only, not the creation runs)

### Backtesting:
NOTE: The backtesting is downloading data from yfinance for now...

engine.py: has the basic entry and exit signal matrix creating along with ATR based stop loss, initial capital and protfolio risk pct.
indic_lib.py: has all the indicators that can be using in the indicators.py
indicator.py: is appending the indicators to the pandas dataframe for main.py to use
loader.py: loading the data directly from yfinance (can be made to redirect itself to the local data base that is stored)
main.py: it has the signals and the logics train and test data (though the train test split has no affect on the algo right now)
report.py: has the function which will create a comprehensive report for the trades that have been executed.

Bash
python update.py
python main.py

## 🤝 Collaboration & Discussions
This project is an open scratchpad for quantitative research. If you have suggestions algorithms (e.g., Fractional Kelly Criterion), backtesting edge cases, or database optimization tricks, feel free to open an Issue, submit a Pull Request, or drop your thoughts in the Discussions tab!
