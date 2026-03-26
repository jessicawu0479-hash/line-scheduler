import requests
import os

# LINE Bot 權杖
LINE_TOKEN = os.getenv("LINE_TOKEN")

# 測試用 User ID（你的 LINE Bot 好友的 User ID）
TEST_USER_ID = os.getenv("TEST_USER_ID")  # 先在 Railway Variables 裡設定

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
    print(f"Sent to {user_id}: {r.status_code}, response: {r.text}")

def main():
    print("Running test LINE message...")
    send_line(TEST_USER_ID, "🚀 測試訊息，LINE Bot 成功！")

if __name__ == "__main__":
    main()
 
