import requests
import os

# 讀環境變數
LINE_TOKEN = os.getenv("LINE_TOKEN")
TEST_USER_ID = os.getenv("TEST_USER_ID")  # 你的 LINE User ID，用於測試

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
    print("Running test LINE message...")
    send_line(TEST_USER_ID, "🚀 測試訊息，LINE Bot 成功！")

if __name__ == "__main__":
    main()
