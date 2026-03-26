import pandas as pd
import requests
from datetime import datetime, timedelta
import pytz
import os

LINE_TOKEN = os.getenv("LINE_TOKEN")
SHEET_URL = os.getenv("SHEET_URL")

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
    requests.post(url, headers=headers, json=data)

def main():
    now = datetime.now(tz)

    if now.strftime("%H:%M") != "13:00":
        print("Not test time yet")
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
