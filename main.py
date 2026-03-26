import pandas as pd
import requests
from datetime import datetime, timedelta
import pytz
import os

# ====== 環境變數 ======
LINE_TOKEN = os.getenv("LINE_TOKEN")        # LINE Channel Access Token
SHEET_URL = os.getenv("SHEET_URL")          # Google Sheet CSV 連結
tz = pytz.timezone("Asia/Taipei")           # 台北時間

# ====== 測試模式開關 ======
TEST_MODE = True  # True = 立即發送，不檢查時間；False = 每天 20:30 發送

# ====== 發送 LINE 訊息函式 ======
def send_line(user_id, message):
    if not user_id.startswith("U"):
        print(f"跳過無效 User ID: {user_id}")
        return
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
    print(f"Sent to {user_id}: {r.status_code}, response: {r.text}")

# ====== 主程式 ======
def main():
    now = datetime.now(tz)
    
    if not TEST_MODE:
        # 每天 20:30 自動發送
        if now.hour != 20 or now.minute < 30 or now.minute > 31:
            print(f"目前時間 {now.strftime('%H:%M:%S')}，尚未到 20:30，不發送訊息")
            return

    # 讀取 Google Sheet CSV
    try:
        df = pd.read_csv(SHEET_URL)
    except Exception as e:
        print("讀取 Google Sheet 失敗:", e)
        return

    # 如果測試模式就抓今天排班，否則抓明日
    target_date = (now + timedelta(days=0 if TEST_MODE else 1)).strftime("%Y-%m-%d")
    schedule = df[df["日期"] == target_date]

    if schedule.empty:
        print(f"{'今天' if TEST_MODE else '明日'} ({target_date}) 沒有排班資料")
        return

    # 發送訊息
    for _, row in schedule.iterrows():
        message = f"""📢 {'今天' if TEST_MODE else '明日'}排班提醒
👤 {row['姓名']}
📅 {target_date}
🕐 {row['班別']}

請準時出勤 ✅"""
        send_line(row["LINE_ID"], message)

# ====== 執行 ======
if __name__ == "__main__":
    main()
