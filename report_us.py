import os, json, requests
from datetime import datetime, timedelta

# --- 初始化 ---
GEMINI_KEY = os.getenv("GEMINI_API_KEY")
DISCORD_URL = os.getenv("DISCORD_WEBHOOK_URL")

def generate_report():
    if not os.path.exists('stock_data.json'): return
    with open('stock_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    tw_time = (datetime.utcnow() + timedelta(hours=8)).strftime('%Y-%m-%d %H:%M')
    
    # 【核心升級：深度美股戰略指令】
    prompt = f"""
    你是總帥的美股首席戰略官。禁止任何廢話與問候，直接進入「硬核戰報」。
    
    【情報數據】: {json.dumps(data, ensure_ascii=False)}
    【戰略防線】: 
    - 根據美股持股做出分析
    
    
    【戰報結構要求】:
    1. 📡 **美股戰情總結**: 用一句話定調昨日美股盤勢（如：多頭反攻、空頭壓制、高檔震盪）。
    2. 📊 **標的深度透視**: 針對 持股列出精確價格，並分析其走勢是否偏離防線。    
    3. 💡 **風險預判**: 簡評今日可能影響市場的宏觀趨勢。
    
    語氣：專業、精確、冷酷。禁止使用軟弱字眼，改用「指令」、「執行」、「埋伏」。
    """
    
    api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_KEY}"
    try:
        response = requests.post(api_url, json={"contents": [{"parts": [{"text": prompt}]}]}, timeout=30)
        report = response.json()["candidates"][0]["content"]["parts"][0]["text"]
        
        full_msg = f"🇺🇸 **【美股晨間硬核戰報 - {tw_time}】**\n{report}"
        # 分段發送確保不截斷
        for i in range(0, len(full_msg), 1900):
            requests.post(DISCORD_URL, json={"content": full_msg[i:i+1900]})
            
        with open("report_us.md", "w", encoding="utf-8") as f: f.write(full_msg)
    except Exception as e:
        print(f"美股分析失敗: {e}")

if __name__ == "__main__": generate_report()
