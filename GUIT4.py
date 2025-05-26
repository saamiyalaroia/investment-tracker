import json
import yfinance as yf
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

FILENAME = "portfolio.json"
SECTOR_OPTIONS = [
    "Consumer Staples", "Energy", "Materials", "Industrials", "Utilities",
    "Healthcare", "Financials", "Consumer discretionary", "Tech",
    "Communication services", "Real estate", "ETF"
]

# Load portfolio from file
def load_portfolio():
    print("Loading portfolio from file...")
    try:
        with open(FILENAME, 'r') as f:
            data = json.load(f)
            print(f"Loaded portfolio: {data}")
            return data
    except FileNotFoundError:
        print("Portfolio file not found. Starting with empty portfolio.")
        return {}

# Save portfolio to file
def save_portfolio(portfolio):
    print(f"Saving portfolio to file: {portfolio}")
    with open(FILENAME, 'w') as f:
        json.dump(portfolio, f, indent=2)

# Update the display in the listbox
def update_portfolio_display():
    print("Updating portfolio display...")
    tree.delete(*tree.get_children())
    for ticker, info in portfolio.items():
        print(f"Displaying: {ticker}, {info}")
        tree.insert('', 'end', values=(ticker, info['entry_price'], info['shares']))

# Add a new holding
def add_holding():
    ticker = ticker_entry.get().strip().upper()
    print(f"Adding holding for ticker: {ticker}")
    try:
        entry_price = float(entry_price_entry.get())
        shares = float(shares_entry.get())
        portfolio[ticker] = {
            "entry_price": entry_price,
            "shares": shares,
            "sector": None
        }
        print(f"Added: {ticker}, Entry Price: {entry_price}, Shares: {shares}")
        messagebox.showinfo("Success", f"✅ {ticker} added to portfolio.")
        update_portfolio_display()
    except ValueError as e:
        print(f"Error adding holding: {e}")
        messagebox.showerror("Error", "❌ Invalid input. Please enter numeric values.")

# Assign sector tag to holding
def assign_sector():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Warning", "Please select a holding to tag.")
        return
    ticker = tree.item(selected[0])['values'][0]
    if ticker not in portfolio:
        return
    tag = simpledialog.askstring("Assign Sector", f"Enter sector for {ticker} (e.g. Tech):\nOptions: {', '.join(SECTOR_OPTIONS)}")
    if tag and tag in SECTOR_OPTIONS:
        portfolio[ticker]['sector'] = tag
        messagebox.showinfo("Tagged", f"✅ {ticker} tagged as {tag}.")
    else:
        messagebox.showerror("Error", "Invalid sector tag.")

# Show pie chart by sector
def sector_summary():
    sector_totals = {}
    for ticker, info in portfolio.items():
        if info.get("sector") is None:
            continue
        data = yf.Ticker(ticker).history(period="1d")
        if not data.empty:
            price = data['Close'].dropna().iloc[-1]
            value = price * info['shares']
            sector_totals[info['sector']] = sector_totals.get(info['sector'], 0) + value

    if not sector_totals:
        messagebox.showinfo("No Data", "No sector tags or valid prices found.")
        return

    fig, ax = plt.subplots()
    ax.pie(sector_totals.values(), labels=sector_totals.keys(), autopct='%1.1f%%', startangle=140)
    ax.set_title("Portfolio Allocation by Sector")

    win = tk.Toplevel(root)
    win.title("Sector Summary")
    canvas = FigureCanvasTkAgg(fig, master=win)
    canvas.draw()
    canvas.get_tk_widget().pack()

# Delete a holding
def delete_holding():
    selected = tree.selection()
    if selected:
        ticker = tree.item(selected[0])['values'][0]
        print(f"Deleting holding: {ticker}")
        if ticker in portfolio:
            del portfolio[ticker]
            messagebox.showinfo("Deleted", f"🗑️ {ticker} removed from portfolio.")
            update_portfolio_display()
    else:
        print("No holding selected to delete.")
        messagebox.showwarning("Warning", "Please select a holding to delete.")

# View performance using most recent available close
def view_performance():
    if not portfolio:
        print("Attempted to view performance on empty portfolio.")
        messagebox.showerror("Error", "Portfolio is empty.")
        return

    rows = []
    total_gain = 0.0

    for ticker, info in portfolio.items():
        print(f"Checking performance for: {ticker}")
        entry = info['entry_price']
        shares = info['shares']
        data = yf.Ticker(ticker).history(period="5d")
        print(f"Data retrieved: {data}")
        if not data.empty:
            close = data['Close'].dropna().iloc[-1]
            pct = ((close - entry) / entry) * 100
            gain = (close - entry) * shares
            total_gain += gain
            rows.append([ticker, f"{entry:.2f}", f"{close:.2f}", f"{shares:.2f}", f"{pct:+.2f}%", f"{gain:+.2f}"])
        else:
            rows.append([ticker, "N/A", "N/A", f"{shares:.2f}", "N/A", "N/A"])

    sign = '+' if total_gain >= 0 else '-'
    summary = f"Total Gain/Loss: {sign}${abs(total_gain):.2f}"
    show_performance_gui(rows, summary)

# GUI performance window
def show_performance_gui(rows, summary):
    perf_window = tk.Toplevel(root)
    perf_window.title("Portfolio Performance")
    perf_window.geometry("750x400")

    tree_perf = ttk.Treeview(perf_window, columns=("Ticker", "Entry", "Close", "Shares", "Return", "Gain"), show='headings')
    for col in ("Ticker", "Entry", "Close", "Shares", "Return", "Gain"):
        tree_perf.heading(col, text=col)
        tree_perf.column(col, width=100)

    for row in rows:
        tag = 'gain' if not row[5].startswith('-') else 'loss'
        tree_perf.insert('', 'end', values=row, tags=(tag,))

    tree_perf.tag_configure('gain', foreground='green')
    tree_perf.tag_configure('loss', foreground='red')

    tree_perf.pack(fill='both', expand=True, pady=10)
    tk.Label(perf_window, text=summary, font=('Arial', 12, 'bold')).pack(pady=10)

# Summary window
def show_summary():
    if not portfolio:
        messagebox.showinfo("Summary", "Portfolio is empty.")
        return

    total_invested = sum(info['entry_price'] * info['shares'] for info in portfolio.values())
    total_gain = 0.0
    for ticker, info in portfolio.items():
        data = yf.Ticker(ticker).history(period="5d")
        if not data.empty:
            close = data['Close'].dropna().iloc[-1]
            gain = (close - info['entry_price']) * info['shares']
            total_gain += gain

    gain_sign = '+' if total_gain >= 0 else '-'
    summary_text = f"Total Invested: ${total_invested:.2f}\nTotal Gain/Loss: {gain_sign}${abs(total_gain):.2f}"
    messagebox.showinfo("Portfolio Summary", summary_text)

# Save and exit
def save_and_exit():
    print("Exiting and saving portfolio...")
    save_portfolio(portfolio)
    root.quit()

# GUI layout
portfolio = load_portfolio()

root = tk.Tk()
root.title("Investment Portfolio Tracker")
root.geometry("600x600")

frame = tk.Frame(root)
frame.pack(pady=10)

# Entry fields
ticker_entry = tk.Entry(frame, width=10)
ticker_entry.grid(row=0, column=1)
tk.Label(frame, text="Ticker").grid(row=0, column=0)

entry_price_entry = tk.Entry(frame, width=10)
entry_price_entry.grid(row=0, column=3)
tk.Label(frame, text="Entry Price").grid(row=0, column=2)

shares_entry = tk.Entry(frame, width=10)
shares_entry.grid(row=0, column=5)
tk.Label(frame, text="Shares").grid(row=0, column=4)

# Buttons
tk.Button(frame, text="Add", command=add_holding).grid(row=0, column=6, padx=5)
tk.Button(root, text="Delete Selected", command=delete_holding).pack(pady=5)
tk.Button(root, text="Assign Tag", command=assign_sector).pack(pady=5)
tk.Button(root, text="View Performance", command=view_performance).pack(pady=5)
tk.Button(root, text="Summary", command=show_summary).pack(pady=5)
tk.Button(root, text="Sector Summary", command=sector_summary).pack(pady=5)
tk.Button(root, text="Save and Exit", command=save_and_exit).pack(pady=10)

# Portfolio display
tree = ttk.Treeview(root, columns=("Ticker", "Entry Price", "Shares"), show='headings')
tree.heading("Ticker", text="Ticker")
tree.heading("Entry Price", text="Entry Price")
tree.heading("Shares", text="Shares")
tree.pack(pady=10)

update_portfolio_display()
root.mainloop()
