import os, json, urllib.request
from datetime import datetime, timedelta

# 抓取 API Key
GEMINI_KEY = os.getenv("GEMINI_API_KEY", "").strip()

def run():
    now_tw = datetime.utcnow() + timedelta(hours=8)
    
    # 讀取剛才抓好的統一大檔案
    if not os.path.exists("stock_data.json"):
        print("Error: Missing stock_data.json")
        return
        
    with open("stock_data.json", 'r', encoding='utf-8') as f:
        market_data = json.load(f)

    if not GEMINI_KEY:
        print("Fatal: Missing GEMINI_API_KEY")
        return
    
    prompt = f"你是 Vicky 的首席投資顧問。請根據以下數據(晨間美股)進行戰略分析，給出具體建議，語氣強勢且精簡，禁止廢話：\n\n{json.dumps(market_data, ensure_ascii=False)}"

    # 使用內建模組直接呼叫 Gemini 2.0 (完全不需要 google 套件)
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_KEY}"
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})

    try:
        print("Requesting US analysis via Gemini 2.0 (Built-in engine)...")
        with urllib.request.urlopen(req) as response:
            res_body = response.read()
            res_json = json.loads(res_body)
            content = res_json["candidates"][0]["content"]["parts"][0]["text"]
        
        # 只寫入 MD 檔，Discord 發送邏輯已徹底移除
        with open("report_us.md", "w", encoding="utf-8") as f:
            f.write(f"# 📡 Vicky 晨間美股戰報 - {now_tw.strftime('%Y-%m-%d %H:%M')}\n\n{content}")
        print("Success! Generated report_us.md")

    except Exception as e:
        print(f"Gemini API Error: {e}")

if __name__ == "__main__":
    run()
