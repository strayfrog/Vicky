import os
import json
import requests
import google.generativeai as genai
from datetime import datetime

# ==========================================
# 1. 安全金鑰設定 (僅保留 Gemini)
# ==========================================
GOOGLE_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

def generate_report():
    try:
        # 讀取剛剛 fetch_data.py 產出的數據
        with open('stock_data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # --- 【Vicky 專屬戰略標的】 ---
        # 只針對這些標的進行分析
        vicky_us_list = ["SPY", "VT", "GRAB", "AVGO", "GOOGL", "NVDA", "CRWD", "PLTR", "RBRK"]
        us_data = {k: v for k, v in data['stocks'].items() if k in vicky_us_list or k in ["DJI", "IXIC", "SOX", "GSPC"]}

        # ==========================================
        # 2. Vicky 專屬 Prompt (調整為高成長股戰術風)
        # ==========================================
        model = genai.GenerativeModel("gemini-1.5-flash")
        
        prompt = f"""
        你是 Vicky 的美股戰略官。請根據以下數據進行硬核分析：
        1. 簡評四大指數(DJI, IXIC, SOX, GSPC)的位階。
        2. 針對高成長核心標的：PLTR、CRWD、RBRK、NVDA 進行點評。
        3. 判斷今日盤勢是否適合執行「見綠點射」戰術。
        4. 語氣要冷靜、專業、精確。
        
        數據內容：{json.dumps(us_data, ensure_ascii=False)}
        """

        response = model.generate_content(prompt)
        report_content = response.text
        
        tw_time = datetime.now().strftime("%Y-%m-%d %H:%M")
        full_msg = f"🇺🇸 **【Vicky 美股晨間戰報 - {tw_time}】**\n\n{report_content}"

        # ==========================================
        # 3. 寫入檔案 (取代 Discord 推送)
        # ==========================================
        with open('report_us.md', 'w', encoding='utf-8') as f:
            f.write(full_msg)
            
        print("✅ Vicky 美股戰報已產出至 report_us.md")

    except Exception as e:
        print(f"❌ 產出報告失敗: {e}")

if __name__ == "__main__":
    generate_report()
