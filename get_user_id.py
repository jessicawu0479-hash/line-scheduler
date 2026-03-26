from flask import Flask, request

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    print("收到 LINE 訊息事件：")
    print(data)  # JSON 裡會有 source.userId
    return "OK"

if __name__ == "__main__":
    # 這裡不用改 port，Railway 會自動分配
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
