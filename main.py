import pandas as pd
import requests
from datetime import datetime, timedelta
import pytz
import os

# === 環境變數設定 ===
LINE_TOKEN = os.getenv("X8sckZVqHlNPSa4O2ND6lGBAVfj+FEvFVEXaQdIIf3w7y6m0Yc+xNUffWvV/+I8xxcuxrT/h6GwDE4rR7QjR/IrSebZ6C2J+E0qlQreY6h62e0TNcyq4R8Xzia4NsESp87wVDf7cZnUSdZVIkdPbsAdB04t89/1O/w1cDnyilFU=")   # 你的 Channel Access Token
SHEET_URL = os.getenv("https://docs.google.com/spreadsheets/d/e/2PACX-1vTA1sQ9_UO7XzFtW7fAI4gjCmOBOfIKD6ZrcF5nKH0s7fZOkVBoFBa-YoTTvEN1gTuK8VHRpkWHDnCw/pub?gid=0&single=true&output=csv")     # Google Sheet CSV 連結

# === 台灣時區 ===
tz = pytz.timezone("Asia/Taipei")

def send_line(user_id, message):
    url = "https://api.line.me/v2/bot/message/push"
    headers = {
        "Authorization": f"Bearer {LINE_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "to": user_id,
        "messages": [{"type": "text", "text": message}]
    }
    r = requests.post(url, headers=headers, json=data)
    print(f"Sent to {user_id}: {r.status_code}")

def main():
    now = datetime.now(tz)
    
    # 只在 20:30 執行
    if now.strftime("%H:%M") != "20:30":
        print(f"Not 20:30 yet. Current time: {now.strftime('%H:%M')}")
        return

    df = pd.read_csv(SHEET_URL)
    tomorrow = (now + timedelta(days=1)).strftime("%Y-%m-%d")

    filtered = df[df["日期"] == tomorrow]

    for _, row in filtered.iterrows():
        msg = f"""📢 明日排班提醒
👤 {row['姓名']}
📅 {tomorrow}
🕐 {row['班別']}

請準時出勤 ✅"""
        send_line(row["LINE_ID"], msg)

if __name__ == "__main__":
    main()
