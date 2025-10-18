import os
import requests
from flask import Flask, request, render_template_string

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

app = Flask(__name__)

HTML_PAGE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DESCO Balance Checker</title>
    <style>
        body {font-family: Arial; background: #f0f4f9; text-align: center; padding-top: 80px;}
        h1 {color: #333;}
        input {padding: 10px; font-size: 16px; margin: 10px;}
        button {padding: 10px 20px; background: #0078D7; color: white; border: none; border-radius: 6px;}
        .result {margin-top: 20px; font-size: 18px; color: #222;}
    </style>
</head>
<body>
    <h1>⚡ DESCO Balance Checker ⚡</h1>
    <form method="post">
        <input type="text" name="account" placeholder="Enter DESCO Account No" required>
        <button type="submit">Check Balance</button>
    </form>
    {% if balance is not none %}
        <div class="result">💡 Balance: {{ balance }}</div>
    {% endif %}
</body>
</html>
'''

def fetch_balance(account_no):
    url = "https://prepaid.desco.org.bd/api/unified/customer/getBalance"
    try:
        res = requests.get(url, params={'accountNo': account_no}, verify=False)
        data = res.json()
        inner = data.get("data")
        if inner and "balance" in inner:
            return inner["balance"]
        return None
    except Exception as e:
        print("Error fetching:", e)
        return None

@app.route("/", methods=["GET", "POST"])
def index():
    balance = None
    if request.method == "POST":
        acc = request.form.get("account")
        balance = fetch_balance(acc)
    return render_template_string(HTML_PAGE, balance=balance)

@app.route(f"/{os.getenv('TELEGRAM_BOT_TOKEN')}", methods=["POST"])
def telegram_webhook():
    data = request.get_json()
    if not data or "message" not in data:
        return "ok"

    chat_id = data["message"]["chat"]["id"]
    text = data["message"].get("text", "")

    if text.lower() in ["/check", "/balance"]:
        acc = os.getenv("ACCOUNT_NO")
        bal = fetch_balance(acc)
        msg = f"💡 Current DESCO Balance: {bal}" if bal else "⚠️ Could not fetch balance."
        send_telegram_message(chat_id, msg)
    elif text.lower().startswith("/check "):
        acc = text.split(" ", 1)[1]
        bal = fetch_balance(acc)
        msg = f"💡 Balance for {acc}: {bal}" if bal else "⚠️ Could not fetch balance for {acc}."
        send_telegram_message(chat_id, msg)
    else:
        send_telegram_message(chat_id, "Send /check or /check <account_no> to get balance.")

    return "ok"

def send_telegram_message(chat_id, text):
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    try:
        requests.post(url, json={"chat_id": chat_id, "text": text})
    except Exception as e:
        print("Telegram error:", e)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
