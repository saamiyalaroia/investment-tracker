# investment-tracker
A simple Python application to help you track and manage your stock investments.

---

### 📁 `README.md`

````markdown
# 📊 Stock Portfolio Tracker GUI

A desktop application built in Python to help you track and manage your stock investments. The GUI allows users to input ticker symbols, entry prices, and share amounts, and stores this data locally in a JSON file. Live data is retrieved using `yfinance`, and portfolio visuals are generated with `matplotlib`.

## 🚀 Features

- 📥 Add custom stocks to your portfolio
- 🗂 Save and load portfolio data from a local JSON file
- 📉 Fetch real-time stock data using Yahoo Finance
- 📊 Visualize portfolio holdings with interactive charts
- 🗑 Remove stocks from your portfolio

## 🛠 Technologies Used

- Python 3.x
- `tkinter` — GUI framework
- `yfinance` — stock market data
- `matplotlib` — charting
- `json` — local data storage

## 📸 GUI Preview

*(Insert a screenshot of the GUI here)*

## 🔧 Installation

1. **Clone this repository**
   ```bash
   git clone https://github.com/your-username/your-repo-name.git
   cd your-repo-name
````

2. **Install dependencies**

   ```bash
   pip install yfinance matplotlib
   ```

3. **Run the application**

   ```bash
   python GUIT4.py
   ```

## 📂 Data Storage

* All user portfolio data is saved in a local file named `portfolio.json`.
* This file is created automatically in the same directory on first run.

## ✅ How to Use

1. Open the app.
2. Enter a stock ticker (e.g., `AAPL`), entry price, and number of shares.
3. Click **Add Holding** to save it to your portfolio.
4. Use the **Delete** or **Update** options to modify holdings.
   

