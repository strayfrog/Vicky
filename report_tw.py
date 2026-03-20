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
        vicky_tw_list = ["2454", "6257", "2882", "2887", "2884", "2890", "00878", "00713", "006208"]
        tw_data = {
            "stocks": {k: v for k, v in data['stocks'].items() if k in vicky_tw_list or k == "TWII"},
            "institutional_investors": data.get('institutional_investors', {})
        }

        # ==========================================
        # 2. Vicky 專屬台股 Prompt
        # ==========================================
        model = genai.GenerativeModel("gemini-1.5-flash")
        
        prompt = f"""
        你是 Vicky 的台股戰略官。請根據以下數據進行精確分析：
        1. 簡評大盤(TWII)位階與今日法人籌碼動向。
        2. 針對核心標的：2454(聯發科)、6257(矽格)、以及金融股(2882, 2887等)進行點評。
        3. 觀察高股息ETF(00878, 00713)與006208的配置狀態。
        4. 語氣要冷靜、專業、像一名戰略傳令兵。
        
        數據內容：{json.dumps(tw_data, ensure_ascii=False)}
        """

        response = model.generate_content(prompt)
        report_content = response.text
        
        tw_time = datetime.now().strftime("%Y-%m-%d %H:%M")
        full_msg = f"🇹🇼 **【Vicky 台股盤後戰報 - {tw_time}】**\n\n{report_content}"

        # ==========================================
        # 3. 寫入檔案 (取代 Discord 推送)
        # ==========================================
        with open('report_tw.md', 'w', encoding='utf-8') as f:
            f.write(full_msg)
            
        print("✅ Vicky 台股戰報已成功寫入 report_tw.md")

    except Exception as e:
        print(f"❌ 台股報告產出失敗: {e}")

if __name__ == "__main__":
    generate_report()
