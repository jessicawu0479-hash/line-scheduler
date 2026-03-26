import pandas as pd
import requests
from datetime import datetime, timedelta
import pytz
import os
import time

# ====== 環境變數 ======
LINE_TOKEN = os.getenv("LINE_TOKEN")
SHEET_URL = os.getenv("SHEET_URL")

tz = pytz.timezone("Asia/Taipei")

# ====== 測試模式 ======
TEST_MODE = False  # True = 立即發送（測試用）

# ====== 防止重複發送 ======
last_sent_keys = set()

# ====== 發送 LINE 訊息 ======
def send_line(user_id, message):
    if not user_id or not str(user_id).startswith("U"):
        print(f"❌ 無效 User ID，跳過: {user_id}")
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

    try:
        r = requests.post(url, headers=headers, json=data)
        print(f"📤 Sent to {user_id}: {r.status_code}, {r.text}")
    except Exception as e:
        print("❌ 發送失敗:", e)

# ====== 發送排班 ======
def send_schedule(target_date, title):
    try:
        df = pd.read_csv(SHEET_URL)
    except Exception as e:
        print("❌ 讀取 Google Sheet 失敗:", e)
        return

    schedule = df[df["日期"] == target_date]

    if schedule.empty:
        print(f"📭 {target_date} 沒有排班資料")
        return

    for _, row in schedule.iterrows():
        message = f"""{title}
👤 {row['姓名']}
📅 {target_date}
🕐 {row['班別']}

請務必準時出勤✅"""

        send_line(row["LINE_ID"], message)

# ====== 主程式 ======
def main():
    now = datetime.now(tz)
    today_str = now.strftime("%Y-%m-%d")

    print(f"⏰ 現在時間: {now.strftime('%Y-%m-%d %H:%M:%S')}")

    # ===== 測試模式 =====
    if TEST_MODE:
        send_schedule(today_str, "🧪 測試排班提醒")
        return

    # ===== 晚上 20:30（明日提醒）=====
    if now.hour == 20 and now.minute == 30:
        key = today_str + "_night"
        if key in last_sent_keys:
            return

        last_sent_keys.add(key)

        target_date = (now + timedelta(days=1)).strftime("%Y-%m-%d")
        print("📢 發送明日排班")

        send_schedule(target_date, "📢明日晨抽提醒📢")

    # ===== 早上 06:00（今日提醒）=====
    elif now.hour == 6 and now.minute == 0:
        key = today_str + "_morning"
        if key in last_sent_keys:
            return

        last_sent_keys.add(key)

        print("🌅 發送今日排班")

        send_schedule(today_str, "🌅今日晨抽提醒!!!（請準時出勤）")

# ====== 持續運行（Railway 必備）======
if __name__ == "__main__":
    while True:
        main()
        time.sleep(60)  # 每60秒檢查一次
