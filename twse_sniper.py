import yfinance as yf
import json
import os

# --- VICKY 專屬標的 ---
US_STOCKS = ["SPY", "VT", "GRAB", "AVGO", "GOOGL", "NVDA", "CRWD", "PLTR", "RBRK"]
US_INDICES = {"道瓊": "^DJI", "納斯達克": "^IXIC", "費半": "^SOX", "S&P500": "^GSPC"}

TW_STOCKS = ["2454.TW", "6257.TW", "2882.TW", "2887.TW", "2884.TW", "2890.TW", "00878.TW", "00713.TW", "006208.TW"]
TW_INDICES = {"台股大盤": "^TWII"}
# -----------------------------------

def get_market_summary(tickers, rename_map=None):
    data = {}
    for ticker in tickers:
        try:
            stock = yf.Ticker(ticker)
            hist = stock.history(period="2d")
            if len(hist) >= 2:
                current = hist['Close'].iloc[-1]
                prev = hist['Close'].iloc[-2]
                change = ((current - prev) / prev) * 100
                name = rename_map.get(ticker, ticker) if rename_map else ticker
                data[name] = {"price": round(current, 2), "change_%": round(change, 2)}
        except Exception as e:
            print(f"Error fetching {ticker}: {e}")
    return data

def run():
    print("Fetching All Market Data...")
    
    # 🎯 關鍵修正：把所有數據包裝在同一個大字典裡，對標原本的架構
    all_data = {
        "US_Indices": get_market_summary(list(US_INDICES.values()), {v:k for k,v in US_INDICES.items()}),
        "US_Stocks": get_market_summary(US_STOCKS),
        "TW_Indices": get_market_summary(list(TW_INDICES.values()), {v:k for k,v in TW_INDICES.items()}),
        "TW_Stocks": get_market_summary(TW_STOCKS),
        "Note": "註：三大法人買賣超數據未包含在內(yfinance無支援)"
    }
    
    # 🎯 關鍵修正：統一寫入 stock_data.json！
    with open("stock_data.json", "w", encoding="utf-8") as f:
        json.dump(all_data, f, ensure_ascii=False, indent=2)

    print("Data Update Complete.")

if __name__ == "__main__":
    run()
