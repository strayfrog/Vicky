import os, json
from datetime import datetime, timedelta
from google import genai

GEMINI_KEY = os.getenv("GEMINI_API_KEY", "").strip()

def run():
    now_tw = datetime.utcnow() + timedelta(hours=8)
    
    if not os.path.exists("data_tw.json"):
        print("Error: Missing data_tw.json")
        return
        
    with open("data_tw.json", 'r', encoding='utf-8') as f:
        market_data = json.load(f)

    if not GEMINI_KEY:
        print("Fatal: Missing GEMINI_API_KEY")
        return
    
    client = genai.Client(api_key=GEMINI_KEY)
    prompt = f"你是 Vicky 的首席投資顧問。請根據以下數據(盤後台股)進行戰略分析，給出具體建議，語氣強勢且精簡，禁止廢話：\n\n{json.dumps(market_data, ensure_ascii=False)}"

    try:
        print("Requesting TW analysis via Gemini 2.0...")
        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=prompt
        )
        
        with open("report_tw.md", "w", encoding="utf-8") as f:
            f.write(f"# 📡 Vicky 盤後台股戰報 - {now_tw.strftime('%Y-%m-%d %H:%M')}\n\n{response.text}")
        print("Success! Generated report_tw.md")

    except Exception as e:
        print(f"Gemini API Error: {e}")

if __name__ == "__main__":
    run()
